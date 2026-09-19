package com.wxyz.eyerest

import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Test

class TimerEngineTest {
    private var now = 0L

    private fun engine(restSeconds: Int = 40, workSeconds: Int = 1_200) =
        TimerEngine(TimerConfig(restSeconds, workSeconds)) { now }

    @Test
    fun initialStateIsPausedAtBeginningOfRest() {
        val snapshot = engine().snapshot()

        assertEquals(TimerPhase.REST, snapshot.phase)
        assertFalse(snapshot.running)
        assertEquals(40, snapshot.remainingSeconds)
        assertEquals(40, snapshot.totalSeconds)
        assertEquals(0, snapshot.completedRests)
    }

    @Test
    fun firstStartEmitsRestStarted() {
        val result = engine().start()

        assertTrue(result.snapshot.running)
        assertEquals(listOf<TimerEvent>(TimerEvent.PhaseStarted(TimerPhase.REST)), result.events)
    }

    @Test
    fun pauseAndResumePreserveRemainingTime() {
        val timer = engine()
        timer.start()
        now = 12_400

        val paused = timer.pause()
        assertFalse(paused.running)
        assertEquals(28, paused.remainingSeconds)

        now = 50_000
        val resumed = timer.start()
        assertTrue(resumed.snapshot.running)
        assertTrue(resumed.events.isEmpty())

        now = 60_000
        assertEquals(18, timer.tick().snapshot.remainingSeconds)
    }

    @Test
    fun reachingRestEndStartsWorkUsingAbsoluteTime() {
        val timer = engine(restSeconds = 10, workSeconds = 60)
        timer.start()
        now = 10_000

        val result = timer.tick()

        assertEquals(TimerPhase.WORK, result.snapshot.phase)
        assertEquals(60, result.snapshot.remainingSeconds)
        assertEquals(1, result.snapshot.completedRests)
        assertEquals(listOf<TimerEvent>(TimerEvent.PhaseStarted(TimerPhase.WORK)), result.events)
    }

    @Test
    fun delayedTickCanCrossMultiplePhasesWithoutDrift() {
        val timer = engine(restSeconds = 10, workSeconds = 20)
        timer.start()
        now = 65_000

        val result = timer.tick()

        assertEquals(TimerPhase.REST, result.snapshot.phase)
        assertEquals(5, result.snapshot.remainingSeconds)
        assertEquals(2, result.snapshot.completedRests)
        assertEquals(
            listOf<TimerEvent>(
                TimerEvent.PhaseStarted(TimerPhase.WORK),
                TimerEvent.PhaseStarted(TimerPhase.REST),
                TimerEvent.PhaseStarted(TimerPhase.WORK),
                TimerEvent.PhaseStarted(TimerPhase.REST),
                TimerEvent.FiveSeconds
            ),
            result.events
        )
    }

    @Test
    fun skipMovesToOtherPhaseAndPreservesRunningState() {
        val timer = engine()
        timer.start()

        val runningSkip = timer.skip()
        assertEquals(TimerPhase.WORK, runningSkip.snapshot.phase)
        assertTrue(runningSkip.snapshot.running)
        assertEquals(1, runningSkip.snapshot.completedRests)

        timer.pause()
        val pausedSkip = timer.skip()
        assertEquals(TimerPhase.REST, pausedSkip.snapshot.phase)
        assertFalse(pausedSkip.snapshot.running)
    }

    @Test
    fun restGuidanceEventsFireWhenThresholdsAreCrossed() {
        val timer = engine(restSeconds = 40)
        timer.start()

        now = 20_000
        assertEquals(listOf<TimerEvent>(TimerEvent.Halfway), timer.tick().events)

        now = 35_000
        assertEquals(listOf<TimerEvent>(TimerEvent.FiveSeconds), timer.tick().events)

        now = 37_000
        assertEquals(listOf<TimerEvent>(TimerEvent.Countdown(3)), timer.tick().events)
        now = 38_000
        assertEquals(listOf<TimerEvent>(TimerEvent.Countdown(2)), timer.tick().events)
        now = 39_000
        assertEquals(listOf<TimerEvent>(TimerEvent.Countdown(1)), timer.tick().events)
    }

    @Test
    fun delayedRestTickEmitsEveryCrossedCountdownCue() {
        val timer = engine(restSeconds = 40)
        timer.start()
        now = 35_000
        timer.tick()
        now = 39_200

        assertEquals(
            listOf<TimerEvent>(
                TimerEvent.Countdown(3),
                TimerEvent.Countdown(2),
                TimerEvent.Countdown(1)
            ),
            timer.tick().events
        )
    }

    @Test
    fun stopReturnsToReadyRestState() {
        val timer = engine()
        timer.start()
        now = 5_000

        val stopped = timer.stop()

        assertFalse(stopped.running)
        assertEquals(TimerPhase.REST, stopped.phase)
        assertEquals(40, stopped.remainingSeconds)
        assertEquals(0, stopped.completedRests)
    }
}

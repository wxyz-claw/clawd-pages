package com.wxyz.eyerest

import kotlin.math.max


enum class TimerPhase {
    REST,
    WORK
}

data class TimerConfig(
    val restSeconds: Int = 40,
    val workSeconds: Int = 1_200
)

data class TimerSnapshot(
    val phase: TimerPhase,
    val running: Boolean,
    val remainingSeconds: Int,
    val totalSeconds: Int,
    val completedRests: Int
)

sealed interface TimerEvent {
    data class PhaseStarted(val phase: TimerPhase) : TimerEvent
    data object Halfway : TimerEvent
    data object FiveSeconds : TimerEvent
    data class Countdown(val seconds: Int) : TimerEvent
}

data class TickResult(
    val snapshot: TimerSnapshot,
    val events: List<TimerEvent> = emptyList()
)

class TimerEngine(
    initialConfig: TimerConfig = TimerConfig(),
    private val nowMillis: () -> Long,
    initialSnapshot: TimerSnapshot? = null
) {
    private var config = initialConfig
    private var phase = initialSnapshot?.phase ?: TimerPhase.REST
    private var running = initialSnapshot?.running ?: false
    private var totalSeconds = initialSnapshot?.totalSeconds ?: durationFor(phase)
    private var remainingSeconds = initialSnapshot?.remainingSeconds ?: totalSeconds
    private var completedRests = initialSnapshot?.completedRests ?: 0
    private var endAtMillis = if (running) nowMillis() + remainingSeconds * 1_000L else 0L
    private var previousRemaining = remainingSeconds
    private var phaseHasStarted = initialSnapshot?.let {
        it.running || it.completedRests > 0 || it.remainingSeconds < it.totalSeconds
    } ?: false

    fun snapshot(): TimerSnapshot = TimerSnapshot(
        phase = phase,
        running = running,
        remainingSeconds = remainingSeconds,
        totalSeconds = totalSeconds,
        completedRests = completedRests
    )

    fun start(): TickResult {
        if (running) return tick()

        running = true
        endAtMillis = nowMillis() + remainingSeconds * 1_000L
        previousRemaining = remainingSeconds
        val events = if (phaseHasStarted) {
            emptyList()
        } else {
            phaseHasStarted = true
            listOf<TimerEvent>(TimerEvent.PhaseStarted(phase))
        }
        return TickResult(snapshot(), events)
    }

    fun pause(): TimerSnapshot {
        if (running) {
            tick()
            running = false
            endAtMillis = 0L
            previousRemaining = remainingSeconds
        }
        return snapshot()
    }

    fun skip(): TickResult {
        val wasRunning = running
        val events = mutableListOf<TimerEvent>()
        switchPhase(nowMillis(), carryEndTime = false, events = events)
        running = wasRunning
        phaseHasStarted = wasRunning
        if (!wasRunning) {
            endAtMillis = 0L
            events.clear()
        }
        return TickResult(snapshot(), events)
    }

    fun stop(): TimerSnapshot {
        running = false
        phase = TimerPhase.REST
        totalSeconds = config.restSeconds
        remainingSeconds = totalSeconds
        completedRests = 0
        endAtMillis = 0L
        previousRemaining = remainingSeconds
        phaseHasStarted = false
        return snapshot()
    }

    fun updateConfig(newConfig: TimerConfig): TimerSnapshot {
        config = newConfig
        if (!running && !phaseHasStarted) {
            totalSeconds = durationFor(phase)
            remainingSeconds = totalSeconds
            previousRemaining = remainingSeconds
        }
        return snapshot()
    }

    fun tick(): TickResult {
        if (!running) return TickResult(snapshot())

        val now = nowMillis()
        val events = mutableListOf<TimerEvent>()

        while (now >= endAtMillis) {
            switchPhase(now, carryEndTime = true, events = events)
        }

        val currentRemaining = secondsUntil(endAtMillis, now)
        if (phase == TimerPhase.REST) {
            appendRestGuidance(previousRemaining, currentRemaining, totalSeconds, events)
        }
        remainingSeconds = currentRemaining
        previousRemaining = currentRemaining

        return TickResult(snapshot(), events)
    }

    private fun switchPhase(
        now: Long,
        carryEndTime: Boolean,
        events: MutableList<TimerEvent>
    ) {
        if (phase == TimerPhase.REST) {
            completedRests += 1
            phase = TimerPhase.WORK
        } else {
            phase = TimerPhase.REST
        }

        totalSeconds = durationFor(phase)
        remainingSeconds = totalSeconds
        previousRemaining = totalSeconds
        endAtMillis = if (carryEndTime) {
            endAtMillis + totalSeconds * 1_000L
        } else {
            now + totalSeconds * 1_000L
        }
        phaseHasStarted = true
        events += TimerEvent.PhaseStarted(phase)
    }

    private fun durationFor(target: TimerPhase): Int = when (target) {
        TimerPhase.REST -> config.restSeconds
        TimerPhase.WORK -> config.workSeconds
    }

    private fun secondsUntil(endMillis: Long, now: Long): Int {
        val millis = max(0L, endMillis - now)
        return ((millis + 999L) / 1_000L).toInt()
    }

    private fun appendRestGuidance(
        previous: Int,
        current: Int,
        total: Int,
        events: MutableList<TimerEvent>
    ) {
        val halfway = total / 2
        if (halfway > 5 && previous > halfway && current <= halfway) {
            events += TimerEvent.Halfway
        }
        if (previous > 5 && current <= 5) {
            events += TimerEvent.FiveSeconds
        }
        for (second in 3 downTo 1) {
            if (previous > second && current <= second) {
                events += TimerEvent.Countdown(second)
            }
        }
    }
}

package com.wxyz.eyerest

import org.junit.Assert.assertEquals
import org.junit.Test

class FormattersTest {
    @Test
    fun formatsDurationWithTwoDigitMinutesAndSeconds() {
        assertEquals("00:00", formatDuration(0))
        assertEquals("01:05", formatDuration(65))
        assertEquals("20:00", formatDuration(1_200))
    }

    @Test
    fun clampsUserDurationsToSupportedRange() {
        assertEquals(TimerConfig(5, 60), clampConfig(1, 0))
        assertEquals(TimerConfig(300, 10_800), clampConfig(999, 999))
        assertEquals(TimerConfig(40, 1_200), clampConfig(40, 20))
    }

    @Test
    fun buildsReadableNotificationText() {
        val rest = TimerSnapshot(TimerPhase.REST, true, 40, 40, 0)
        val work = TimerSnapshot(TimerPhase.WORK, false, 75, 1_200, 1)

        assertEquals("Eye rest · 00:40", notificationText(rest))
        assertEquals("Focus paused · 01:15", notificationText(work))
    }
}

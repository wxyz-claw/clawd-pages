package com.wxyz.eyerest

fun formatDuration(seconds: Int): String {
    val safe = seconds.coerceAtLeast(0)
    return "%02d:%02d".format(safe / 60, safe % 60)
}

fun clampConfig(restSeconds: Int, workMinutes: Int): TimerConfig = TimerConfig(
    restSeconds = restSeconds.coerceIn(5, 300),
    workSeconds = workMinutes.coerceIn(1, 180) * 60
)

fun notificationText(snapshot: TimerSnapshot): String {
    val base = when (snapshot.phase) {
        TimerPhase.REST -> "Eye rest"
        TimerPhase.WORK -> "Focus"
    }
    val state = if (snapshot.running) base else "$base paused"
    return "$state · ${formatDuration(snapshot.remainingSeconds)}"
}

package com.wxyz.eyerest

import android.content.Context

object TimerStore {
    private const val PREFS = "eye_rest_timer_state"
    private const val PHASE = "phase"
    private const val RUNNING = "running"
    private const val REMAINING = "remaining"
    private const val TOTAL = "total"
    private const val COMPLETED_RESTS = "completed_rests"

    fun save(context: Context, snapshot: TimerSnapshot) {
        context.getSharedPreferences(PREFS, Context.MODE_PRIVATE)
            .edit()
            .putString(PHASE, snapshot.phase.name)
            .putBoolean(RUNNING, snapshot.running)
            .putInt(REMAINING, snapshot.remainingSeconds)
            .putInt(TOTAL, snapshot.totalSeconds)
            .putInt(COMPLETED_RESTS, snapshot.completedRests)
            .apply()
    }

    fun load(context: Context): TimerSnapshot? {
        val prefs = context.getSharedPreferences(PREFS, Context.MODE_PRIVATE)
        val phaseName = prefs.getString(PHASE, null) ?: return null
        val phase = runCatching { TimerPhase.valueOf(phaseName) }.getOrNull() ?: return null
        val total = prefs.getInt(TOTAL, 0)
        val remaining = prefs.getInt(REMAINING, 0)
        if (total <= 0 || remaining < 0) return null

        return TimerSnapshot(
            phase = phase,
            running = prefs.getBoolean(RUNNING, false),
            remainingSeconds = remaining.coerceAtMost(total),
            totalSeconds = total,
            completedRests = prefs.getInt(COMPLETED_RESTS, 0).coerceAtLeast(0)
        )
    }
}

package com.wxyz.eyerest

import android.content.Context


data class UserSettings(
    val restSeconds: Int = 40,
    val workMinutes: Int = 20,
    val voiceEnabled: Boolean = true,
    val chimeEnabled: Boolean = true,
    val breakMusicEnabled: Boolean = true
) {
    fun timerConfig(): TimerConfig = clampConfig(restSeconds, workMinutes)
}

object AppSettings {
    private const val PREFS = "eye_rest_settings"
    private const val REST_SECONDS = "rest_seconds"
    private const val WORK_MINUTES = "work_minutes"
    private const val VOICE_ENABLED = "voice_enabled"
    private const val CHIME_ENABLED = "chime_enabled"
    private const val BREAK_MUSIC_ENABLED = "break_music_enabled"

    fun load(context: Context): UserSettings {
        val prefs = context.getSharedPreferences(PREFS, Context.MODE_PRIVATE)
        return normalize(
            UserSettings(
                restSeconds = prefs.getInt(REST_SECONDS, 40),
                workMinutes = prefs.getInt(WORK_MINUTES, 20),
                voiceEnabled = prefs.getBoolean(VOICE_ENABLED, true),
                chimeEnabled = prefs.getBoolean(CHIME_ENABLED, true),
                breakMusicEnabled = prefs.getBoolean(BREAK_MUSIC_ENABLED, true)
            )
        )
    }

    fun save(context: Context, settings: UserSettings): UserSettings {
        val normalized = normalize(settings)
        context.getSharedPreferences(PREFS, Context.MODE_PRIVATE)
            .edit()
            .putInt(REST_SECONDS, normalized.restSeconds)
            .putInt(WORK_MINUTES, normalized.workMinutes)
            .putBoolean(VOICE_ENABLED, normalized.voiceEnabled)
            .putBoolean(CHIME_ENABLED, normalized.chimeEnabled)
            .putBoolean(BREAK_MUSIC_ENABLED, normalized.breakMusicEnabled)
            .apply()
        return normalized
    }

    private fun normalize(settings: UserSettings): UserSettings = settings.copy(
        restSeconds = settings.restSeconds.coerceIn(5, 300),
        workMinutes = settings.workMinutes.coerceIn(1, 180)
    )
}

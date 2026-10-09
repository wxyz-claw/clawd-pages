package com.wxyz.eyerest

import android.content.Context
import android.media.AudioAttributes
import android.media.AudioManager
import android.media.MediaPlayer
import android.media.ToneGenerator
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.speech.tts.TextToSpeech
import android.speech.tts.UtteranceProgressListener

enum class VoicePrompt(val recording: Int, val text: String) {
    REST_START(R.raw.rest_start, "Take a moment. Look into the distance."),
    HALFWAY(R.raw.halfway, "Let your eyes relax. Blink gently."),
    FIVE_SECONDS(R.raw.five_seconds, "Just a few more seconds."),
    THREE(0, ""), TWO(0, ""), ONE(0, ""),
    WORK_START(R.raw.work_start, "All set. Ease back into your day.")
}

/** Bundled narration is the offline default. TTS is only a playback-error fallback. */
class VoiceGuide(
    context: Context,
    private val onUnavailable: () -> Unit = {},
    private val onSpeechActive: (Boolean) -> Unit = {}
) {
    private val appContext = context.applicationContext
    private val handler = Handler(Looper.getMainLooper())
    private val attributes = AudioAttributes.Builder()
        .setUsage(AudioAttributes.USAGE_MEDIA)
        .setContentType(AudioAttributes.CONTENT_TYPE_SPEECH).build()
    private var player: MediaPlayer? = null
    private var tts: TextToSpeech? = null
    private var ready = false
    private var closed = false
    private var activeSpeech = false
    private var generation = 0
    private var pending: Pair<Int, VoicePrompt>? = null
    private var tone: ToneGenerator? = null

    fun play(prompt: VoicePrompt, voiceEnabled: Boolean, chimeEnabled: Boolean) {
        if (closed) return
        // Countdown is a quiet, optional chime, never overlapping spoken numbers.
        if (prompt.recording == 0) {
            if (chimeEnabled) chime(prompt)
            return
        }
        cancel()
        val token = generation
        if (chimeEnabled && prompt in listOf(VoicePrompt.REST_START, VoicePrompt.WORK_START)) chime(prompt)
        if (!voiceEnabled) return
        setSpeechActive(true)
        val next = MediaPlayer()
        player = next
        // Covers both a stalled decoder and a TTS engine that never initializes.
        handler.postDelayed({ if (generation == token && activeSpeech) {
            cancel(); onUnavailable()
        } }, 8_000L)
        try {
            next.setAudioAttributes(attributes)
            appContext.resources.openRawResourceFd(prompt.recording).use {
                next.setDataSource(it.fileDescriptor, it.startOffset, it.length)
            }
            next.setOnPreparedListener { if (current(token, next)) it.start() }
            next.setOnCompletionListener { if (current(token, next)) finish() }
            next.setOnErrorListener { _, _, _ ->
                if (current(token, next)) { releasePlayer(); fallback(prompt, token) }
                true
            }
            next.prepareAsync()
        } catch (_: Exception) {
            releasePlayer()
            fallback(prompt, token)
        }
    }

    fun cancel() {
        generation++
        pending = null
        handler.removeCallbacksAndMessages(null)
        releasePlayer()
        tts?.stop()
        tone?.stopTone()
        setSpeechActive(false)
    }

    fun close() {
        cancel()
        closed = true
        tone?.release(); tone = null
        tts?.shutdown(); tts = null; ready = false
    }

    private fun setSpeechActive(value: Boolean) { activeSpeech = value; onSpeechActive(value) }

    private fun current(token: Int, candidate: MediaPlayer) = !closed && generation == token && player === candidate
    private fun releasePlayer() { player?.release(); player = null }
    private fun finish() { releasePlayer(); pending = null; setSpeechActive(false) }

    private fun fallback(prompt: VoicePrompt, token: Int) {
        if (closed || token != generation) return
        if (ready) { speak(prompt, token); return }
        pending = token to prompt
        if (tts != null) return
        tts = TextToSpeech(appContext) { status ->
            handler.post {
                if (closed) return@post
                val engine = tts ?: return@post
                if (status != TextToSpeech.SUCCESS) {
                    val failedCurrent = pending?.first == generation
                    pending = null; engine.shutdown(); tts = null; setSpeechActive(false)
                    if (failedCurrent) onUnavailable()
                    return@post
                }
                val offlineVoice = engine.voices?.filter {
                    it.locale.language == "en" && !it.isNetworkConnectionRequired &&
                        TextToSpeech.Engine.KEY_FEATURE_NOT_INSTALLED !in it.features
                }?.maxByOrNull { it.quality * 2 - it.latency }
                if (offlineVoice == null || engine.setVoice(offlineVoice) != TextToSpeech.SUCCESS) {
                    val failedCurrent = pending?.first == generation
                    pending = null; engine.shutdown(); tts = null; setSpeechActive(false)
                    if (failedCurrent) onUnavailable()
                    return@post
                }
                engine.setSpeechRate(.94f); engine.setPitch(1f); engine.setAudioAttributes(attributes)
                engine.setOnUtteranceProgressListener(object : UtteranceProgressListener() {
                    override fun onStart(id: String?) = Unit
                    override fun onDone(id: String?) { handler.post { if (id == "speech-$generation") finish() } }
                    @Deprecated("Deprecated in Java")
                    override fun onError(id: String?) { handler.post {
                        if (id == "speech-$generation") { finish(); onUnavailable() }
                    } }
                })
                ready = true
                pending?.let { (epoch, cue) -> if (epoch == generation) speak(cue, epoch) }
                pending = null
            }
        }
    }

    private fun speak(prompt: VoicePrompt, token: Int) {
        setSpeechActive(true)
        if (tts?.speak(prompt.text, TextToSpeech.QUEUE_FLUSH, Bundle(), "speech-$token") != TextToSpeech.SUCCESS) {
            finish(); onUnavailable()
        }
    }

    private fun chime(prompt: VoicePrompt) {
        runCatching {
            val generator = tone ?: ToneGenerator(AudioManager.STREAM_MUSIC, 25).also { tone = it }
            val kind = when (prompt) {
                VoicePrompt.REST_START -> ToneGenerator.TONE_PROP_BEEP2
                VoicePrompt.WORK_START -> ToneGenerator.TONE_PROP_ACK
                else -> ToneGenerator.TONE_PROP_BEEP
            }
            generator.startTone(kind, 80)
        }
    }
}

package com.wxyz.eyerest

import android.content.Context
import android.media.AudioAttributes
import android.media.AudioManager
import android.media.MediaPlayer
import android.media.ToneGenerator
import android.os.Bundle
import android.speech.tts.TextToSpeech
import android.speech.tts.UtteranceProgressListener
import java.io.File
import java.util.Locale


enum class VoicePrompt(val cacheId: String, val text: String) {
    REST_START(
        "rest_start",
        "Time for an eye break. Look far away and blink slowly."
    ),
    HALFWAY(
        "halfway",
        "Keep looking far away. Relax your eyes."
    ),
    FIVE_SECONDS(
        "five_seconds",
        "Almost done. Five seconds."
    ),
    THREE("three", "Three."),
    TWO("two", "Two."),
    ONE("one", "One."),
    WORK_START(
        "work_start",
        "Eye break complete. Back to work."
    )
}

class VoiceGuide(context: Context) {
    private val appContext = context.applicationContext
    private val voiceDirectory = File(appContext.cacheDir, "eye-rest-voice").apply { mkdirs() }
    private val audioAttributes = AudioAttributes.Builder()
        .setUsage(AudioAttributes.USAGE_MEDIA)
        .setContentType(AudioAttributes.CONTENT_TYPE_SPEECH)
        .build()

    private var textToSpeech: TextToSpeech? = null
    private var ready = false
    private var pendingPrompt: VoicePrompt? = null
    private var player: MediaPlayer? = null
    private var toneGenerator: ToneGenerator? = null

    fun prepare() {
        if (textToSpeech != null) return
        textToSpeech = TextToSpeech(appContext) { status ->
            val engine = textToSpeech
            if (status == TextToSpeech.SUCCESS && engine != null) {
                configure(engine)
                ready = true
                synthesizeMissing(engine)
                pendingPrompt?.also {
                    pendingPrompt = null
                    speakDirect(it)
                }
            }
        }
    }

    fun play(prompt: VoicePrompt, voiceEnabled: Boolean, chimeEnabled: Boolean) {
        if (chimeEnabled) playChime(prompt)
        if (!voiceEnabled) return

        if (!ready) {
            pendingPrompt = prompt
            prepare()
            return
        }

        val file = promptFile(prompt)
        if (file.isFile && file.length() > 44L) {
            if (!playCached(file)) speakDirect(prompt)
        } else {
            speakDirect(prompt)
            textToSpeech?.let { synthesizePrompt(it, prompt) }
        }
    }

    fun close() {
        pendingPrompt = null
        player?.release()
        player = null
        toneGenerator?.release()
        toneGenerator = null
        textToSpeech?.stop()
        textToSpeech?.shutdown()
        textToSpeech = null
        ready = false
    }

    private fun configure(engine: TextToSpeech) {
        engine.language = Locale.US
        engine.setSpeechRate(0.88f)
        engine.setPitch(0.98f)
        engine.setAudioAttributes(audioAttributes)
        val selectedVoice = engine.voices
            ?.filter { it.locale.language.equals("en", ignoreCase = true) }
            ?.sortedWith(
                compareBy<android.speech.tts.Voice> { it.isNetworkConnectionRequired }
                    .thenByDescending { it.quality }
            )
            ?.firstOrNull()
        if (selectedVoice != null) engine.voice = selectedVoice
        engine.setOnUtteranceProgressListener(object : UtteranceProgressListener() {
            override fun onStart(utteranceId: String?) = Unit
            override fun onDone(utteranceId: String?) = Unit
            @Deprecated("Deprecated in Java")
            override fun onError(utteranceId: String?) = Unit
        })
    }

    private fun synthesizeMissing(engine: TextToSpeech) {
        VoicePrompt.entries.forEach { prompt ->
            val file = promptFile(prompt)
            if (!file.isFile || file.length() <= 44L) synthesizePrompt(engine, prompt)
        }
    }

    private fun synthesizePrompt(engine: TextToSpeech, prompt: VoicePrompt) {
        runCatching {
            engine.synthesizeToFile(
                prompt.text,
                Bundle(),
                promptFile(prompt),
                "cache-${prompt.cacheId}"
            )
        }
    }

    private fun speakDirect(prompt: VoicePrompt) {
        textToSpeech?.speak(
            prompt.text,
            TextToSpeech.QUEUE_FLUSH,
            Bundle(),
            "speak-${prompt.cacheId}"
        )
    }

    private fun playCached(file: File): Boolean = runCatching {
        player?.release()
        val nextPlayer = MediaPlayer().apply {
            setAudioAttributes(audioAttributes)
            setDataSource(file.absolutePath)
            setOnCompletionListener { completed ->
                completed.release()
                if (player === completed) player = null
            }
            setOnErrorListener { failed, _, _ ->
                failed.release()
                if (player === failed) player = null
                true
            }
            prepare()
            start()
        }
        player = nextPlayer
        true
    }.getOrDefault(false)

    private fun playChime(prompt: VoicePrompt) {
        val tone = when (prompt) {
            VoicePrompt.REST_START -> ToneGenerator.TONE_PROP_BEEP2
            VoicePrompt.WORK_START -> ToneGenerator.TONE_PROP_ACK
            else -> ToneGenerator.TONE_PROP_BEEP
        }
        runCatching {
            val generator = toneGenerator ?: ToneGenerator(AudioManager.STREAM_MUSIC, 55).also {
                toneGenerator = it
            }
            generator.startTone(tone, 130)
        }
    }

    private fun promptFile(prompt: VoicePrompt): File =
        File(voiceDirectory, "${prompt.cacheId}.wav")
}

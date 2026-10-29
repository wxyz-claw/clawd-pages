package com.wxyz.eyerest

import android.content.Context
import android.media.AudioAttributes
import android.media.AudioManager
import android.media.MediaPlayer
import android.media.ToneGenerator
import android.os.Bundle
import android.speech.tts.TextToSpeech
import android.speech.tts.UtteranceProgressListener
import android.speech.tts.Voice
import java.io.File
import java.util.Locale


enum class VoicePrompt(val cacheId: String, val text: String) {
    REST_START(
        "rest_start",
        "It's time to rest your eyes. Look into the distance, and let your gaze soften."
    ),
    HALFWAY(
        "halfway",
        "Keep looking far away. Breathe slowly, and relax your eyes."
    ),
    FIVE_SECONDS(
        "five_seconds",
        "Five seconds left. Keep your eyes soft."
    ),
    THREE("three", "Three."),
    TWO("two", "Two."),
    ONE("one", "One."),
    WORK_START(
        "work_start",
        "Nice work. Your eye break is complete. You can return to your screen."
    )
}

class VoiceGuide(
    context: Context,
    private val onSpeechActive: (Boolean) -> Unit = {}
) {
    private val appContext = context.applicationContext
    private val cacheRoot = File(appContext.cacheDir, "eye-rest-voice-v3").apply { mkdirs() }
    private val audioAttributes = AudioAttributes.Builder()
        .setUsage(AudioAttributes.USAGE_MEDIA)
        .setContentType(AudioAttributes.CONTENT_TYPE_SPEECH)
        .build()

    private var textToSpeech: TextToSpeech? = null
    private var ready = false
    private var pendingPrompt: VoicePrompt? = null
    private var player: MediaPlayer? = null
    private var toneGenerator: ToneGenerator? = null
    private var voiceCacheKey = "default"

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

        stopActiveSpeech()
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
        stopActiveSpeech()
        toneGenerator?.release()
        toneGenerator = null
        textToSpeech?.shutdown()
        textToSpeech = null
        ready = false
        onSpeechActive(false)
    }

    private fun configure(engine: TextToSpeech) {
        engine.language = Locale.US
        engine.setSpeechRate(0.94f)
        engine.setPitch(1.01f)
        engine.setAudioAttributes(audioAttributes)

        val selectedVoice = engine.voices
            ?.asSequence()
            ?.filter { it.locale.language.equals("en", ignoreCase = true) }
            ?.maxByOrNull(::voiceScore)

        if (selectedVoice != null) {
            engine.voice = selectedVoice
            voiceCacheKey = selectedVoice.name.hashCode().toUInt().toString(16)
        }

        engine.setOnUtteranceProgressListener(object : UtteranceProgressListener() {
            override fun onStart(utteranceId: String?) {
                if (utteranceId?.startsWith("speak-") == true) onSpeechActive(true)
            }

            override fun onDone(utteranceId: String?) {
                if (utteranceId?.startsWith("speak-") == true) onSpeechActive(false)
            }

            @Deprecated("Deprecated in Java")
            override fun onError(utteranceId: String?) {
                if (utteranceId?.startsWith("speak-") == true) onSpeechActive(false)
            }
        })
    }

    private fun voiceScore(voice: Voice): Int {
        val name = voice.name.lowercase(Locale.US)
        var score = voice.quality * 2 - voice.latency

        score += when (voice.locale.country.uppercase(Locale.US)) {
            "US" -> 80
            "CA", "GB", "AU", "NZ" -> 45
            else -> 10
        }

        if (voice.isNetworkConnectionRequired) score += 45
        if ("natural" in name) score += 180
        if ("neural" in name) score += 180
        if ("wavenet" in name) score += 170
        if ("studio" in name) score += 160
        if ("premium" in name) score += 150
        if ("enhanced" in name) score += 120
        if ("network" in name) score += 50
        if ("compact" in name || "legacy" in name) score -= 100

        return score
    }

    private fun synthesizeMissing(engine: TextToSpeech) {
        VoicePrompt.entries.forEach { prompt ->
            val file = promptFile(prompt)
            if (!file.isFile || file.length() <= 44L) synthesizePrompt(engine, prompt)
        }
    }

    private fun synthesizePrompt(engine: TextToSpeech, prompt: VoicePrompt) {
        val file = promptFile(prompt)
        file.parentFile?.mkdirs()
        runCatching {
            engine.synthesizeToFile(
                prompt.text,
                Bundle(),
                file,
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
        onSpeechActive(true)
        val nextPlayer = MediaPlayer().apply {
            setAudioAttributes(audioAttributes)
            setDataSource(file.absolutePath)
            setOnCompletionListener { completed ->
                completed.release()
                if (player === completed) player = null
                onSpeechActive(false)
            }
            setOnErrorListener { failed, _, _ ->
                failed.release()
                if (player === failed) player = null
                onSpeechActive(false)
                true
            }
            prepare()
            start()
        }
        player = nextPlayer
        true
    }.getOrElse {
        onSpeechActive(false)
        false
    }

    private fun stopActiveSpeech() {
        player?.release()
        player = null
        textToSpeech?.stop()
        onSpeechActive(false)
    }

    private fun playChime(prompt: VoicePrompt) {
        val tone = when (prompt) {
            VoicePrompt.REST_START -> ToneGenerator.TONE_PROP_BEEP2
            VoicePrompt.WORK_START -> ToneGenerator.TONE_PROP_ACK
            else -> ToneGenerator.TONE_PROP_BEEP
        }
        runCatching {
            val generator = toneGenerator ?: ToneGenerator(AudioManager.STREAM_MUSIC, 45).also {
                toneGenerator = it
            }
            generator.startTone(tone, 110)
        }
    }

    private fun promptFile(prompt: VoicePrompt): File =
        File(File(cacheRoot, voiceCacheKey), "${prompt.cacheId}.wav")
}

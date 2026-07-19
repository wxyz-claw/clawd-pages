package com.wxyz.eyerest

import android.media.AudioAttributes
import android.media.AudioFormat
import android.media.AudioTrack
import kotlin.math.PI
import kotlin.math.exp
import kotlin.math.sin

class BreakMusicPlayer {
    @Volatile
    private var ducked = false

    @Volatile
    private var generation = 0

    @Volatile
    private var track: AudioTrack? = null

    fun setDucked(value: Boolean) {
        ducked = value
    }

    @Synchronized
    fun start() {
        if (track != null) return

        val minBufferBytes = AudioTrack.getMinBufferSize(
            SAMPLE_RATE,
            AudioFormat.CHANNEL_OUT_MONO,
            AudioFormat.ENCODING_PCM_16BIT
        ).coerceAtLeast(BUFFER_SAMPLES * 2)

        val localTrack = AudioTrack.Builder()
            .setAudioAttributes(
                AudioAttributes.Builder()
                    .setUsage(AudioAttributes.USAGE_MEDIA)
                    .setContentType(AudioAttributes.CONTENT_TYPE_MUSIC)
                    .build()
            )
            .setAudioFormat(
                AudioFormat.Builder()
                    .setSampleRate(SAMPLE_RATE)
                    .setEncoding(AudioFormat.ENCODING_PCM_16BIT)
                    .setChannelMask(AudioFormat.CHANNEL_OUT_MONO)
                    .build()
            )
            .setBufferSizeInBytes(minBufferBytes)
            .setTransferMode(AudioTrack.MODE_STREAM)
            .build()

        generation += 1
        val session = generation
        track = localTrack

        Thread({ stream(localTrack, session) }, "EyeRestBreakMusic").apply {
            isDaemon = true
            start()
        }
    }

    @Synchronized
    fun stop() {
        generation += 1
        ducked = false
        val oldTrack = track
        track = null
        runCatching { oldTrack?.pause() }
        runCatching { oldTrack?.flush() }
    }

    fun close() {
        stop()
    }

    private fun stream(localTrack: AudioTrack, session: Int) {
        val buffer = ShortArray(BUFFER_SAMPLES)
        var sampleIndex = 0L
        var duckGain = 1.0

        try {
            localTrack.play()
            while (generation == session && track === localTrack) {
                for (index in buffer.indices) {
                    val timeSeconds = sampleIndex.toDouble() / SAMPLE_RATE
                    val targetDuckGain = if (ducked) 0.18 else 1.0
                    duckGain += (targetDuckGain - duckGain) * DUCK_SMOOTHING
                    val sample = ambientSample(timeSeconds) * duckGain
                    buffer[index] = (sample.coerceIn(-0.92, 0.92) * Short.MAX_VALUE).toInt().toShort()
                    sampleIndex += 1
                }

                val written = localTrack.write(
                    buffer,
                    0,
                    buffer.size,
                    AudioTrack.WRITE_BLOCKING
                )
                if (written < 0) break
            }
        } finally {
            runCatching { localTrack.stop() }
            runCatching { localTrack.release() }
            synchronized(this) {
                if (track === localTrack) track = null
            }
        }
    }

    private fun ambientSample(timeSeconds: Double): Double {
        val loopTime = timeSeconds % LOOP_SECONDS
        val chordIndex = (loopTime / CHORD_SECONDS).toInt() % CHORDS.size
        val chordTime = loopTime % CHORD_SECONDS
        val fade = smoothStep(((chordTime - CROSSFADE_START) / CROSSFADE_SECONDS).coerceIn(0.0, 1.0))

        val currentPad = chordPad(CHORDS[chordIndex], timeSeconds)
        val nextPad = chordPad(CHORDS[(chordIndex + 1) % CHORDS.size], timeSeconds)
        val blendedPad = currentPad * (1.0 - fade) + nextPad * fade

        val breathing = 0.82 + 0.18 * sin(TAU * timeSeconds / 8.0)
        val bellEnvelope = exp(-2.1 * chordTime)
        val bellFrequency = MELODY[chordIndex]
        val bell = (
            sin(TAU * bellFrequency * timeSeconds) +
                0.32 * sin(TAU * bellFrequency * 2.01 * timeSeconds)
            ) * bellEnvelope * 0.055

        return (blendedPad * breathing + bell) * MASTER_GAIN
    }

    private fun chordPad(frequencies: DoubleArray, timeSeconds: Double): Double {
        var value = 0.0
        frequencies.forEachIndexed { index, frequency ->
            val phase = index * 0.73
            value += sin(TAU * frequency * timeSeconds + phase) * 0.19
            value += sin(TAU * frequency * 2.0 * timeSeconds + phase * 0.5) * 0.025
        }
        return value / frequencies.size
    }

    private fun smoothStep(value: Double): Double = value * value * (3.0 - 2.0 * value)

    companion object {
        private const val SAMPLE_RATE = 22_050
        private const val BUFFER_SAMPLES = 1_024
        private const val CHORD_SECONDS = 4.0
        private const val LOOP_SECONDS = 16.0
        private const val CROSSFADE_START = 2.8
        private const val CROSSFADE_SECONDS = 1.2
        private const val MASTER_GAIN = 0.58
        private const val DUCK_SMOOTHING = 0.0012
        private const val TAU = 2.0 * PI

        private val CHORDS = arrayOf(
            doubleArrayOf(130.81, 164.81, 196.00, 246.94),
            doubleArrayOf(110.00, 130.81, 164.81, 196.00),
            doubleArrayOf(87.31, 130.81, 164.81, 220.00),
            doubleArrayOf(98.00, 146.83, 196.00, 220.00)
        )

        private val MELODY = doubleArrayOf(659.25, 523.25, 440.00, 587.33)
    }
}

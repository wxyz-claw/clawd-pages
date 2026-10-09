package com.wxyz.eyerest

import android.app.Notification
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.app.Service
import android.content.Context
import android.content.Intent
import android.content.BroadcastReceiver
import android.content.IntentFilter
import android.content.pm.ServiceInfo
import android.graphics.Color
import android.os.Build
import android.os.Handler
import android.os.IBinder
import android.os.Looper
import android.os.PowerManager
import android.os.SystemClock
import android.media.AudioAttributes
import android.media.AudioFocusRequest
import android.media.AudioManager

class EyeRestService : Service() {
    private val handler = Handler(Looper.getMainLooper())
    private lateinit var engine: TimerEngine
    private lateinit var voiceGuide: VoiceGuide
    private lateinit var breakMusicPlayer: BreakMusicPlayer
    private lateinit var wakeLock: PowerManager.WakeLock
    private var settings = UserSettings()
    private var foregroundActive = false
    private var lastPublishedSecond = -1
    private lateinit var audioManager: AudioManager
    private lateinit var focusRequest: AudioFocusRequest
    private var hasAudioFocus = false
    private var speechActive = false
    private var pauseReason = ""
    private var noisyRegistered = false
    private val noisyReceiver = object : BroadcastReceiver() {
        override fun onReceive(context: Context?, intent: Intent?) {
            if (intent?.action == AudioManager.ACTION_AUDIO_BECOMING_NOISY && engine.snapshot().running &&
                (settings.voiceEnabled || settings.chimeEnabled || settings.breakMusicEnabled)) {
                pauseReason = "Audio disconnected. Resume when you're ready."
                pause()
            }
        }
    }

    private val ticker = object : Runnable {
        override fun run() {
            val result = engine.tick()
            syncBreakMusic(result.snapshot)
            handleEvents(result.events)
            publish(result.snapshot)
            if (result.snapshot.running) handler.postDelayed(this, TICK_MILLIS)
        }
    }

    override fun onCreate() {
        super.onCreate()
        createNotificationChannel()
        settings = AppSettings.load(this)
        audioManager = getSystemService(AudioManager::class.java)
        focusRequest = AudioFocusRequest.Builder(AudioManager.AUDIOFOCUS_GAIN_TRANSIENT_MAY_DUCK)
            .setAudioAttributes(AudioAttributes.Builder().setUsage(AudioAttributes.USAGE_MEDIA)
                .setContentType(AudioAttributes.CONTENT_TYPE_SPEECH).build())
            .setOnAudioFocusChangeListener({ change ->
                if (change < 0 && engine.snapshot().running) {
                    pauseReason = "Audio interrupted. Resume when you're ready."
                    pause()
                }
            }, handler).build()
        if (Build.VERSION.SDK_INT >= 33) registerReceiver(noisyReceiver,
            IntentFilter(AudioManager.ACTION_AUDIO_BECOMING_NOISY), Context.RECEIVER_NOT_EXPORTED)
        else registerReceiver(noisyReceiver, IntentFilter(AudioManager.ACTION_AUDIO_BECOMING_NOISY))
        noisyRegistered = true
        engine = TimerEngine(
            initialConfig = settings.timerConfig(),
            initialSnapshot = TimerStore.load(this)
        ) { SystemClock.elapsedRealtime() }
        breakMusicPlayer = BreakMusicPlayer()
        voiceGuide = VoiceGuide(this, onUnavailable = {
            handler.post {
                if (engine.snapshot().running) { pauseReason = "Voice unavailable. Resume with voice off in Options."; pause() }
            }
        }) { speechActive ->
            this.speechActive = speechActive
            breakMusicPlayer.setDucked(speechActive)
            handler.postDelayed({
                if (!this.speechActive && !(engine.snapshot().running && engine.snapshot().phase == TimerPhase.REST && settings.breakMusicEnabled)) releaseAudioFocus()
            }, 150L)
        }
        val powerManager = getSystemService(PowerManager::class.java)
        wakeLock = powerManager.newWakeLock(
            PowerManager.PARTIAL_WAKE_LOCK,
            "$packageName:EyeRestTimer"
        ).apply { setReferenceCounted(false) }
    }

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        // A sticky service restart restores an active session, never resumes a pause.
        if (intent == null && !engine.snapshot().running) { stopSelf(); return START_NOT_STICKY }
        when (intent?.action ?: ACTION_START_OR_RESUME) {
            ACTION_START_OR_RESUME -> startOrResume()
            ACTION_PAUSE -> pause()
            ACTION_SKIP -> skip()
            ACTION_STOP -> stopSession()
            ACTION_REFRESH_SETTINGS -> refreshSettings()
        }
        return if (engine.snapshot().running) START_STICKY else START_NOT_STICKY
    }

    override fun onBind(intent: Intent?): IBinder? = null

    override fun onDestroy() {
        releaseWakeLock()
        breakMusicPlayer.close()
        voiceGuide.close()
        handler.removeCallbacksAndMessages(null)
        releaseAudioFocus()
        if (noisyRegistered) unregisterReceiver(noisyReceiver)
        super.onDestroy()
    }

    private fun startOrResume() {
        pauseReason = ""
        settings = AppSettings.load(this)
        engine.updateConfig(settings.timerConfig())
        val result = engine.start()
        ensureForeground(result.snapshot)
        acquireWakeLock()
        syncBreakMusic(result.snapshot)
        handleEvents(result.events)
        publish(result.snapshot, force = true)
        handler.removeCallbacks(ticker)
        handler.postDelayed(ticker, TICK_MILLIS)
    }

    private fun pause() {
        val snapshot = engine.pause()
        handler.removeCallbacks(ticker)
        releaseWakeLock()
        breakMusicPlayer.stop()
        voiceGuide.cancel()
        releaseAudioFocus()
        ensureForeground(snapshot)
        publish(snapshot, force = true)
    }

    private fun skip() {
        voiceGuide.cancel()
        val result = engine.skip()
        ensureForeground(result.snapshot)
        if (result.snapshot.running) {
            acquireWakeLock()
            handler.removeCallbacks(ticker)
            handler.postDelayed(ticker, TICK_MILLIS)
        } else {
            releaseWakeLock()
        }
        syncBreakMusic(result.snapshot)
        handleEvents(result.events)
        publish(result.snapshot, force = true)
    }

    private fun stopSession() {
        handler.removeCallbacks(ticker)
        releaseWakeLock()
        breakMusicPlayer.stop()
        voiceGuide.cancel()
        releaseAudioFocus()
        val snapshot = engine.stop()
        publish(snapshot, force = true)
        stopForeground(STOP_FOREGROUND_REMOVE)
        foregroundActive = false
        stopSelf()
    }

    private fun refreshSettings() {
        settings = AppSettings.load(this)
        if (engine.snapshot().running && !foregroundActive) startOrResume()
        if (!settings.voiceEnabled) voiceGuide.cancel()
        val snapshot = engine.updateConfig(settings.timerConfig())
        syncBreakMusic(snapshot)
        publish(snapshot, force = true)
        if (!foregroundActive) stopSelf()
    }

    private fun syncBreakMusic(snapshot: TimerSnapshot) {
        if (
            settings.breakMusicEnabled &&
            snapshot.running &&
            snapshot.phase == TimerPhase.REST
        ) {
            if (requestAudioFocus()) runCatching { breakMusicPlayer.start() }.onFailure {
                handler.post {
                    if (engine.snapshot().running) { pauseReason = "Audio unavailable. Resume when you're ready."; pause() }
                }
            }
        } else {
            breakMusicPlayer.stop()
            if (!speechActive) releaseAudioFocus()
        }
    }

    private fun handleEvents(events: List<TimerEvent>) {
        // Only the newest relevant cue may speak after a delayed callback.
        events.takeLast(1).forEach { event ->
            val prompt = when (event) {
                is TimerEvent.PhaseStarted -> when (event.phase) {
                    TimerPhase.REST -> VoicePrompt.REST_START
                    TimerPhase.WORK -> VoicePrompt.WORK_START
                }
                TimerEvent.Halfway -> VoicePrompt.HALFWAY
                TimerEvent.FiveSeconds -> VoicePrompt.FIVE_SECONDS
                is TimerEvent.Countdown -> when (event.seconds) {
                    3 -> VoicePrompt.THREE
                    2 -> VoicePrompt.TWO
                    else -> VoicePrompt.ONE
                }
            }
            if ((settings.voiceEnabled || settings.chimeEnabled) && !requestAudioFocus()) return
            voiceGuide.play(
                prompt = prompt,
                voiceEnabled = settings.voiceEnabled,
                chimeEnabled = settings.chimeEnabled
            )
            if (!speechActive && !settings.breakMusicEnabled) handler.postDelayed({
                if (!speechActive && !(engine.snapshot().running && engine.snapshot().phase == TimerPhase.REST && settings.breakMusicEnabled)) releaseAudioFocus()
            }, 150L)
        }
    }

    private fun publish(snapshot: TimerSnapshot, force: Boolean = false) {
        if (!force && snapshot.remainingSeconds == lastPublishedSecond) return
        lastPublishedSecond = snapshot.remainingSeconds
        TimerStore.save(this, snapshot)
        sendBroadcast(
            Intent(ACTION_STATE_CHANGED)
                .setPackage(packageName)
                .putExtra(EXTRA_PHASE, snapshot.phase.name)
                .putExtra(EXTRA_RUNNING, snapshot.running)
                .putExtra(EXTRA_REMAINING, snapshot.remainingSeconds)
                .putExtra(EXTRA_TOTAL, snapshot.totalSeconds)
                .putExtra(EXTRA_COMPLETED_RESTS, snapshot.completedRests)
                .putExtra(EXTRA_PAUSE_REASON, pauseReason)
        )
        if (foregroundActive) {
            getSystemService(NotificationManager::class.java)
                .notify(NOTIFICATION_ID, buildNotification(snapshot))
        }
    }

    private fun ensureForeground(snapshot: TimerSnapshot) {
        val notification = buildNotification(snapshot)
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
            startForeground(
                NOTIFICATION_ID,
                notification,
                ServiceInfo.FOREGROUND_SERVICE_TYPE_MEDIA_PLAYBACK
            )
        } else {
            startForeground(NOTIFICATION_ID, notification)
        }
        foregroundActive = true
    }

    private fun buildNotification(snapshot: TimerSnapshot): Notification {
        val openApp = PendingIntent.getActivity(
            this,
            100,
            Intent(this, MainActivity::class.java),
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )
        val pauseOrResumeAction = if (snapshot.running) ACTION_PAUSE else ACTION_START_OR_RESUME
        val pauseOrResumeLabel = if (snapshot.running) "Pause" else "Resume"

        return Notification.Builder(this, CHANNEL_ID)
            .setSmallIcon(R.drawable.ic_eye_rest)
            .setColor(Color.rgb(44, 114, 94))
            .setContentTitle("Eye Rest")
            .setContentText(pauseReason.ifEmpty { notificationText(snapshot) })
            .setContentIntent(openApp)
            .setCategory(Notification.CATEGORY_SERVICE)
            .setVisibility(Notification.VISIBILITY_PUBLIC)
            .setOngoing(true)
            .setOnlyAlertOnce(true)
            .setShowWhen(false)
            .addAction(
                Notification.Action.Builder(
                    R.drawable.ic_eye_rest,
                    pauseOrResumeLabel,
                    serviceAction(pauseOrResumeAction, 201)
                ).build()
            )
            .addAction(
                Notification.Action.Builder(
                    R.drawable.ic_eye_rest,
                    "Skip",
                    serviceAction(ACTION_SKIP, 202)
                ).build()
            )
            .addAction(
                Notification.Action.Builder(
                    R.drawable.ic_eye_rest,
                    "Stop",
                    serviceAction(ACTION_STOP, 203)
                ).build()
            )
            .build()
    }

    private fun serviceAction(action: String, requestCode: Int): PendingIntent =
        PendingIntent.getService(
            this,
            requestCode,
            Intent(this, EyeRestService::class.java).setAction(action),
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )

    private fun createNotificationChannel() {
        val channel = NotificationChannel(
            CHANNEL_ID,
            getString(R.string.notification_channel_name),
            NotificationManager.IMPORTANCE_LOW
        ).apply {
            description = getString(R.string.notification_channel_description)
            setSound(null, null)
            enableVibration(false)
            lockscreenVisibility = Notification.VISIBILITY_PUBLIC
        }
        getSystemService(NotificationManager::class.java).createNotificationChannel(channel)
    }

    private fun acquireWakeLock() {
        if (!wakeLock.isHeld) wakeLock.acquire()
    }

    private fun requestAudioFocus(): Boolean {
        if (hasAudioFocus) return true
        hasAudioFocus = audioManager.requestAudioFocus(focusRequest) == AudioManager.AUDIOFOCUS_REQUEST_GRANTED
        if (!hasAudioFocus && engine.snapshot().running) {
            handler.post {
                if (engine.snapshot().running) { pauseReason = "Audio unavailable. Resume when you're ready."; pause() }
            }
        }
        return hasAudioFocus
    }

    private fun releaseAudioFocus() {
        if (hasAudioFocus) audioManager.abandonAudioFocusRequest(focusRequest)
        hasAudioFocus = false
    }

    private fun releaseWakeLock() {
        if (::wakeLock.isInitialized && wakeLock.isHeld) wakeLock.release()
    }

    companion object {
        const val ACTION_START_OR_RESUME = "com.wxyz.eyerest.action.START_OR_RESUME"
        const val ACTION_PAUSE = "com.wxyz.eyerest.action.PAUSE"
        const val ACTION_SKIP = "com.wxyz.eyerest.action.SKIP"
        const val ACTION_STOP = "com.wxyz.eyerest.action.STOP"
        const val ACTION_REFRESH_SETTINGS = "com.wxyz.eyerest.action.REFRESH_SETTINGS"
        const val ACTION_STATE_CHANGED = "com.wxyz.eyerest.action.STATE_CHANGED"

        const val EXTRA_PHASE = "phase"
        const val EXTRA_RUNNING = "running"
        const val EXTRA_REMAINING = "remaining"
        const val EXTRA_TOTAL = "total"
        const val EXTRA_COMPLETED_RESTS = "completed_rests"
        const val EXTRA_PAUSE_REASON = "pause_reason"

        private const val CHANNEL_ID = "eye_rest_timer"
        private const val NOTIFICATION_ID = 202020
        private const val TICK_MILLIS = 1_000L

        fun intent(context: Context, action: String): Intent =
            Intent(context, EyeRestService::class.java).setAction(action)
    }
}

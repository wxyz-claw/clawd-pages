package com.wxyz.eyerest

import android.app.Notification
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.app.Service
import android.content.Context
import android.content.Intent
import android.content.pm.ServiceInfo
import android.graphics.Color
import android.os.Build
import android.os.Handler
import android.os.IBinder
import android.os.Looper
import android.os.PowerManager
import android.os.SystemClock

class EyeRestService : Service() {
    private val handler = Handler(Looper.getMainLooper())
    private lateinit var engine: TimerEngine
    private lateinit var voiceGuide: VoiceGuide
    private lateinit var wakeLock: PowerManager.WakeLock
    private var settings = UserSettings()
    private var foregroundActive = false
    private var lastPublishedSecond = -1

    private val ticker = object : Runnable {
        override fun run() {
            val result = engine.tick()
            handleEvents(result.events)
            publish(result.snapshot)
            if (result.snapshot.running) handler.postDelayed(this, TICK_MILLIS)
        }
    }

    override fun onCreate() {
        super.onCreate()
        createNotificationChannel()
        settings = AppSettings.load(this)
        engine = TimerEngine(
            initialConfig = settings.timerConfig(),
            initialSnapshot = TimerStore.load(this)
        ) { SystemClock.elapsedRealtime() }
        voiceGuide = VoiceGuide(this).also { it.prepare() }
        val powerManager = getSystemService(PowerManager::class.java)
        wakeLock = powerManager.newWakeLock(
            PowerManager.PARTIAL_WAKE_LOCK,
            "$packageName:EyeRestTimer"
        ).apply { setReferenceCounted(false) }
    }

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        when (intent?.action ?: ACTION_START_OR_RESUME) {
            ACTION_START_OR_RESUME -> startOrResume()
            ACTION_PAUSE -> pause()
            ACTION_SKIP -> skip()
            ACTION_STOP -> stopSession()
            ACTION_REFRESH_SETTINGS -> refreshSettings()
        }
        return START_STICKY
    }

    override fun onBind(intent: Intent?): IBinder? = null

    override fun onDestroy() {
        handler.removeCallbacksAndMessages(null)
        releaseWakeLock()
        voiceGuide.close()
        super.onDestroy()
    }

    private fun startOrResume() {
        settings = AppSettings.load(this)
        engine.updateConfig(settings.timerConfig())
        val result = engine.start()
        ensureForeground(result.snapshot)
        acquireWakeLock()
        handleEvents(result.events)
        publish(result.snapshot, force = true)
        handler.removeCallbacks(ticker)
        handler.postDelayed(ticker, TICK_MILLIS)
    }

    private fun pause() {
        val snapshot = engine.pause()
        handler.removeCallbacks(ticker)
        releaseWakeLock()
        ensureForeground(snapshot)
        publish(snapshot, force = true)
    }

    private fun skip() {
        val result = engine.skip()
        ensureForeground(result.snapshot)
        if (result.snapshot.running) {
            acquireWakeLock()
            handler.removeCallbacks(ticker)
            handler.postDelayed(ticker, TICK_MILLIS)
        } else {
            releaseWakeLock()
        }
        handleEvents(result.events)
        publish(result.snapshot, force = true)
    }

    private fun stopSession() {
        handler.removeCallbacks(ticker)
        releaseWakeLock()
        val snapshot = engine.stop()
        publish(snapshot, force = true)
        stopForeground(STOP_FOREGROUND_REMOVE)
        foregroundActive = false
        stopSelf()
    }

    private fun refreshSettings() {
        settings = AppSettings.load(this)
        val snapshot = engine.updateConfig(settings.timerConfig())
        if (foregroundActive) publish(snapshot, force = true)
    }

    private fun handleEvents(events: List<TimerEvent>) {
        events.forEach { event ->
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
            voiceGuide.play(
                prompt = prompt,
                voiceEnabled = settings.voiceEnabled,
                chimeEnabled = settings.chimeEnabled
            )
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
            .setContentText(notificationText(snapshot))
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

        private const val CHANNEL_ID = "eye_rest_timer"
        private const val NOTIFICATION_ID = 202020
        private const val TICK_MILLIS = 250L

        fun intent(context: Context, action: String): Intent =
            Intent(context, EyeRestService::class.java).setAction(action)
    }
}

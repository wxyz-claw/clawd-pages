package com.wxyz.eyerest

import android.Manifest
import android.app.Activity
import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.content.IntentFilter
import android.content.pm.PackageManager
import android.graphics.Color
import android.graphics.Typeface
import android.graphics.drawable.GradientDrawable
import android.os.Build
import android.os.Bundle
import android.text.InputType
import android.view.Gravity
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.CheckBox
import android.widget.EditText
import android.widget.ImageView
import android.widget.LinearLayout
import android.widget.ScrollView
import android.widget.TextView
import android.widget.Toast

class MainActivity : Activity() {
    private lateinit var phaseView: TextView
    private lateinit var clockView: TextView
    private lateinit var detailView: TextView
    private lateinit var primaryButton: Button
    private lateinit var skipButton: Button
    private lateinit var stopButton: Button
    private lateinit var restSecondsInput: EditText
    private lateinit var workMinutesInput: EditText
    private lateinit var voiceCheck: CheckBox
    private lateinit var chimeCheck: CheckBox
    private var receiverRegistered = false
    private var currentSnapshot = TimerSnapshot(
        phase = TimerPhase.REST,
        running = false,
        remainingSeconds = 40,
        totalSeconds = 40,
        completedRests = 0
    )

    private val stateReceiver = object : BroadcastReceiver() {
        override fun onReceive(context: Context?, intent: Intent?) {
            if (intent?.action != EyeRestService.ACTION_STATE_CHANGED) return
            val phase = runCatching {
                TimerPhase.valueOf(
                    intent.getStringExtra(EyeRestService.EXTRA_PHASE) ?: TimerPhase.REST.name
                )
            }.getOrDefault(TimerPhase.REST)
            render(
                TimerSnapshot(
                    phase = phase,
                    running = intent.getBooleanExtra(EyeRestService.EXTRA_RUNNING, false),
                    remainingSeconds = intent.getIntExtra(EyeRestService.EXTRA_REMAINING, 40),
                    totalSeconds = intent.getIntExtra(EyeRestService.EXTRA_TOTAL, 40),
                    completedRests = intent.getIntExtra(EyeRestService.EXTRA_COMPLETED_RESTS, 0)
                )
            )
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(buildContent())
        loadSettingsIntoUi()
        render(
            TimerStore.load(this) ?: TimerSnapshot(
                phase = TimerPhase.REST,
                running = false,
                remainingSeconds = AppSettings.load(this).restSeconds,
                totalSeconds = AppSettings.load(this).restSeconds,
                completedRests = 0
            )
        )
        requestNotificationPermissionIfNeeded()
    }

    override fun onStart() {
        super.onStart()
        if (!receiverRegistered) {
            val filter = IntentFilter(EyeRestService.ACTION_STATE_CHANGED)
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
                registerReceiver(stateReceiver, filter, Context.RECEIVER_NOT_EXPORTED)
            } else {
                @Suppress("DEPRECATION")
                registerReceiver(stateReceiver, filter)
            }
            receiverRegistered = true
        }
        TimerStore.load(this)?.let(::render)
    }

    override fun onStop() {
        if (receiverRegistered) {
            unregisterReceiver(stateReceiver)
            receiverRegistered = false
        }
        super.onStop()
    }

    override fun onRequestPermissionsResult(
        requestCode: Int,
        permissions: Array<out String>,
        grantResults: IntArray
    ) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)
        if (
            requestCode == NOTIFICATION_PERMISSION_REQUEST &&
            grantResults.firstOrNull() != PackageManager.PERMISSION_GRANTED
        ) {
            Toast.makeText(
                this,
                "Allow notifications for reliable lock-screen controls.",
                Toast.LENGTH_LONG
            ).show()
        }
    }

    private fun buildContent(): View {
        val scroll = ScrollView(this).apply {
            isFillViewport = true
            setBackgroundColor(Color.parseColor("#F4FAF5"))
        }
        val root = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            gravity = Gravity.CENTER_HORIZONTAL
            setPadding(dp(24), dp(28), dp(24), dp(36))
        }
        scroll.addView(
            root,
            ViewGroup.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT,
                ViewGroup.LayoutParams.WRAP_CONTENT
            )
        )

        root.addView(ImageView(this).apply {
            setImageResource(R.drawable.ic_eye_rest)
            layoutParams = LinearLayout.LayoutParams(dp(84), dp(84)).apply {
                bottomMargin = dp(12)
            }
        })
        root.addView(label("Eye Rest", 42f, "#527063", Typeface.NORMAL))

        phaseView = label("Ready", 14f, "#6D7E76", Typeface.BOLD).apply {
            isAllCaps = true
            letterSpacing = 0.12f
            layoutParams = LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.WRAP_CONTENT,
                ViewGroup.LayoutParams.WRAP_CONTENT
            ).apply { topMargin = dp(26) }
        }
        root.addView(phaseView)

        clockView = label("00:40", 76f, "#173A31", Typeface.NORMAL).apply {
            typeface = Typeface.create("sans-serif-light", Typeface.NORMAL)
            gravity = Gravity.CENTER
            layoutParams = LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT,
                ViewGroup.LayoutParams.WRAP_CONTENT
            ).apply {
                topMargin = dp(4)
                bottomMargin = dp(6)
            }
        }
        root.addView(clockView)

        detailView = label(
            "Rest first, then focus. Voice guidance continues after the phone locks.",
            16f,
            "#65766F",
            Typeface.NORMAL
        ).apply {
            gravity = Gravity.CENTER
            setLineSpacing(0f, 1.18f)
        }
        root.addView(detailView)

        primaryButton = actionButton("Start timer", primary = true).apply {
            layoutParams = LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT,
                dp(64)
            ).apply {
                topMargin = dp(28)
                bottomMargin = dp(12)
            }
            setOnClickListener {
                saveSettingsFromUi()
                if (currentSnapshot.running) {
                    sendServiceAction(EyeRestService.ACTION_PAUSE)
                } else {
                    requestNotificationPermissionIfNeeded()
                    sendServiceAction(EyeRestService.ACTION_START_OR_RESUME)
                }
            }
        }
        root.addView(primaryButton)

        val secondaryRow = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            gravity = Gravity.CENTER
        }
        skipButton = actionButton("Skip", primary = false).apply {
            setOnClickListener { sendServiceAction(EyeRestService.ACTION_SKIP) }
        }
        stopButton = actionButton("Stop", primary = false, danger = true).apply {
            setOnClickListener { sendServiceAction(EyeRestService.ACTION_STOP) }
        }
        secondaryRow.addView(
            skipButton,
            LinearLayout.LayoutParams(0, dp(52), 1f).apply { marginEnd = dp(6) }
        )
        secondaryRow.addView(
            stopButton,
            LinearLayout.LayoutParams(0, dp(52), 1f).apply { marginStart = dp(6) }
        )
        root.addView(
            secondaryRow,
            LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT,
                ViewGroup.LayoutParams.WRAP_CONTENT
            )
        )

        val settingsCard = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(dp(18), dp(18), dp(18), dp(18))
            background = roundedBackground("#FFFFFF", 22f, "#DCE9DF")
        }
        settingsCard.addView(label("Options", 18f, "#40564D", Typeface.BOLD))

        val durationRow = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            gravity = Gravity.TOP
        }
        restSecondsInput = numberField("40")
        workMinutesInput = numberField("20")
        durationRow.addView(
            fieldGroup("Rest seconds", restSecondsInput),
            LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f).apply {
                marginEnd = dp(8)
            }
        )
        durationRow.addView(
            fieldGroup("Work minutes", workMinutesInput),
            LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f).apply {
                marginStart = dp(8)
            }
        )
        settingsCard.addView(
            durationRow,
            LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT,
                ViewGroup.LayoutParams.WRAP_CONTENT
            ).apply { topMargin = dp(14) }
        )

        voiceCheck = CheckBox(this).apply {
            text = "Voice guidance"
            textSize = 16f
            setTextColor(Color.parseColor("#40564D"))
            setPadding(0, dp(8), 0, 0)
            setOnCheckedChangeListener { _, _ -> settingsChanged() }
        }
        chimeCheck = CheckBox(this).apply {
            text = "Chimes"
            textSize = 16f
            setTextColor(Color.parseColor("#40564D"))
            setOnCheckedChangeListener { _, _ -> settingsChanged() }
        }
        settingsCard.addView(voiceCheck)
        settingsCard.addView(chimeCheck)
        settingsCard.addView(label(
            "The ongoing notification and a partial wake lock keep timing and audio active with the display off. Stop the timer when you are finished to release the wake lock.",
            13f,
            "#72827B",
            Typeface.NORMAL
        ).apply {
            setLineSpacing(0f, 1.16f)
            setPadding(0, dp(8), 0, 0)
        })
        root.addView(
            settingsCard,
            LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT,
                ViewGroup.LayoutParams.WRAP_CONTENT
            ).apply { topMargin = dp(28) }
        )

        restSecondsInput.setOnFocusChangeListener { _, hasFocus ->
            if (!hasFocus) settingsChanged()
        }
        workMinutesInput.setOnFocusChangeListener { _, hasFocus ->
            if (!hasFocus) settingsChanged()
        }

        return scroll
    }

    private fun render(snapshot: TimerSnapshot) {
        currentSnapshot = snapshot
        val ready = !snapshot.running &&
            snapshot.phase == TimerPhase.REST &&
            snapshot.completedRests == 0 &&
            snapshot.remainingSeconds == snapshot.totalSeconds

        phaseView.text = when {
            ready -> "Ready"
            snapshot.phase == TimerPhase.REST && snapshot.running -> "Eye rest"
            snapshot.phase == TimerPhase.WORK && snapshot.running -> "Focus time"
            snapshot.phase == TimerPhase.REST -> "Eye rest paused"
            else -> "Focus paused"
        }
        clockView.text = formatDuration(snapshot.remainingSeconds)
        primaryButton.text = when {
            snapshot.running -> "Pause"
            ready -> "Start timer"
            else -> "Resume"
        }
        detailView.text = when {
            ready -> "Rest first, then focus. Voice guidance continues after the phone locks."
            snapshot.phase == TimerPhase.REST && snapshot.running ->
                "Look far away and blink slowly. The audio will guide you back."
            snapshot.phase == TimerPhase.WORK && snapshot.running ->
                "Work quietly. The next eye rest starts automatically."
            else -> "Timer paused. Resume here or from the lock-screen notification."
        }
    }

    private fun loadSettingsIntoUi() {
        val settings = AppSettings.load(this)
        restSecondsInput.setText(settings.restSeconds.toString())
        workMinutesInput.setText(settings.workMinutes.toString())
        voiceCheck.isChecked = settings.voiceEnabled
        chimeCheck.isChecked = settings.chimeEnabled
    }

    private fun settingsChanged() {
        saveSettingsFromUi()
        if (currentSnapshot.running) sendServiceAction(EyeRestService.ACTION_REFRESH_SETTINGS)
    }

    private fun saveSettingsFromUi(): UserSettings {
        val existing = AppSettings.load(this)
        val saved = AppSettings.save(
            this,
            UserSettings(
                restSeconds = restSecondsInput.text.toString().toIntOrNull()
                    ?: existing.restSeconds,
                workMinutes = workMinutesInput.text.toString().toIntOrNull()
                    ?: existing.workMinutes,
                voiceEnabled = voiceCheck.isChecked,
                chimeEnabled = chimeCheck.isChecked
            )
        )
        restSecondsInput.setText(saved.restSeconds.toString())
        workMinutesInput.setText(saved.workMinutes.toString())
        return saved
    }

    private fun sendServiceAction(action: String) {
        val intent = EyeRestService.intent(this, action)
        if (
            action == EyeRestService.ACTION_START_OR_RESUME &&
            Build.VERSION.SDK_INT >= Build.VERSION_CODES.O
        ) {
            startForegroundService(intent)
        } else {
            startService(intent)
        }
    }

    private fun requestNotificationPermissionIfNeeded() {
        if (
            Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU &&
            checkSelfPermission(Manifest.permission.POST_NOTIFICATIONS) !=
            PackageManager.PERMISSION_GRANTED
        ) {
            requestPermissions(
                arrayOf(Manifest.permission.POST_NOTIFICATIONS),
                NOTIFICATION_PERMISSION_REQUEST
            )
        }
    }

    private fun fieldGroup(title: String, field: EditText): LinearLayout =
        LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            addView(label(title, 13f, "#6C7D75", Typeface.NORMAL))
            addView(
                field,
                LinearLayout.LayoutParams(
                    ViewGroup.LayoutParams.MATCH_PARENT,
                    dp(52)
                ).apply { topMargin = dp(6) }
            )
        }

    private fun numberField(value: String): EditText = EditText(this).apply {
        setText(value)
        inputType = InputType.TYPE_CLASS_NUMBER
        gravity = Gravity.CENTER
        textSize = 18f
        setTextColor(Color.parseColor("#233B34"))
        setSelectAllOnFocus(true)
        background = roundedBackground("#F9FCF9", 14f, "#D7E5DB")
        setPadding(dp(10), 0, dp(10), 0)
    }

    private fun actionButton(
        label: String,
        primary: Boolean,
        danger: Boolean = false
    ): Button = Button(this).apply {
        text = label
        isAllCaps = false
        textSize = if (primary) 22f else 17f
        typeface = Typeface.create("sans-serif", Typeface.BOLD)
        setTextColor(
            Color.parseColor(
                when {
                    primary -> "#FFFFFF"
                    danger -> "#8B3737"
                    else -> "#426154"
                }
            )
        )
        background = roundedBackground(
            fill = if (primary) "#246B58" else "#FFFFFF",
            radius = 28f,
            stroke = if (primary) "#246B58" else "#D7E5DB"
        )
        elevation = if (primary) dp(4).toFloat() else 0f
    }

    private fun label(
        value: String,
        size: Float,
        color: String,
        style: Int
    ): TextView = TextView(this).apply {
        text = value
        textSize = size
        setTextColor(Color.parseColor(color))
        typeface = Typeface.create("sans-serif", style)
        gravity = Gravity.CENTER_HORIZONTAL
    }

    private fun roundedBackground(fill: String, radius: Float, stroke: String): GradientDrawable =
        GradientDrawable().apply {
            shape = GradientDrawable.RECTANGLE
            cornerRadius = dp(radius.toInt()).toFloat()
            setColor(Color.parseColor(fill))
            setStroke(dp(1), Color.parseColor(stroke))
        }

    private fun dp(value: Int): Int =
        (value * resources.displayMetrics.density + 0.5f).toInt()

    companion object {
        private const val NOTIFICATION_PERMISSION_REQUEST = 7301
    }
}

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
import android.widget.FrameLayout
import android.provider.Settings
import android.view.WindowInsets

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
    private lateinit var breakMusicCheck: CheckBox
    private lateinit var ring: TimerRing
    private lateinit var rhythmView: TextView
    private lateinit var notificationNote: Button
    private var loadingSettings = false
    private var optionsExpanded = false
    private var pauseReason = ""
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
            pauseReason = intent.getStringExtra(EyeRestService.EXTRA_PAUSE_REASON).orEmpty()
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
        optionsExpanded = savedInstanceState?.getBoolean("options_expanded") ?: false
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
    }

    // API33+ uses NOT_EXPORTED; the legacy overload is reachable only on older Android.
    @android.annotation.SuppressLint("UnspecifiedRegisterReceiverFlag")
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
        notificationNote.visibility = if (Build.VERSION.SDK_INT >= 33 &&
            checkSelfPermission(Manifest.permission.POST_NOTIFICATIONS) != PackageManager.PERMISSION_GRANTED) View.VISIBLE else View.GONE
    }

    override fun onStop() {
        if (receiverRegistered) {
            unregisterReceiver(stateReceiver)
            receiverRegistered = false
        }
        super.onStop()
    }

    override fun onSaveInstanceState(outState: Bundle) {
        outState.putBoolean("options_expanded", optionsExpanded)
        super.onSaveInstanceState(outState)
    }

    override fun onRequestPermissionsResult(
        requestCode: Int,
        permissions: Array<out String>,
        grantResults: IntArray
    ) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)
        notificationNote.visibility = if (Build.VERSION.SDK_INT >= 33 &&
            checkSelfPermission(Manifest.permission.POST_NOTIFICATIONS) != PackageManager.PERMISSION_GRANTED) View.VISIBLE else View.GONE
        if (
            requestCode == NOTIFICATION_PERMISSION_REQUEST &&
            grantResults.firstOrNull() != PackageManager.PERMISSION_GRANTED
        ) {
            Toast.makeText(
                this,
                "Notifications are off. Enable them in Options for lock-screen controls.",
                Toast.LENGTH_LONG
            ).show()
        }
    }

    private fun buildContent(): View {
        val scroll = ScrollView(this).apply {
            isFillViewport = true
            setBackgroundColor(Color.parseColor("#F4FAF5"))
            clipToPadding = false
            setOnApplyWindowInsetsListener { view, insets ->
                if (Build.VERSION.SDK_INT >= 30) {
                    val safe = insets.getInsets(WindowInsets.Type.systemBars() or WindowInsets.Type.displayCutout())
                    val keyboard = insets.getInsets(WindowInsets.Type.ime()).bottom
                    view.setPadding(safe.left, safe.top, safe.right, maxOf(safe.bottom, keyboard))
                } else {
                    @Suppress("DEPRECATION")
                    view.setPadding(insets.systemWindowInsetLeft, insets.systemWindowInsetTop,
                        insets.systemWindowInsetRight, insets.systemWindowInsetBottom)
                }
                insets
            }
        }
        val root = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            gravity = Gravity.CENTER_HORIZONTAL
            setPadding(dp(24), dp(20), dp(24), dp(24))
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
            importantForAccessibility = View.IMPORTANT_FOR_ACCESSIBILITY_NO
            layoutParams = LinearLayout.LayoutParams(dp(60), dp(60)).apply {
                bottomMargin = dp(8)
            }
        })
        root.addView(label("Eye Rest", 36f, "#527063", Typeface.NORMAL).apply {
            if (Build.VERSION.SDK_INT >= 28) isAccessibilityHeading = true
        })

        phaseView = label("Ready", 14f, "#52655B", Typeface.BOLD).apply {
            isAllCaps = true
            letterSpacing = 0.12f
            accessibilityLiveRegion = View.ACCESSIBILITY_LIVE_REGION_POLITE
            layoutParams = LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.WRAP_CONTENT,
                ViewGroup.LayoutParams.WRAP_CONTENT
            ).apply { topMargin = dp(20) }
        }
        root.addView(phaseView)

        clockView = label("00:40", 72f, "#173A31", Typeface.NORMAL).apply {
            typeface = Typeface.create("sans-serif-light", Typeface.NORMAL)
            gravity = Gravity.CENTER
            setAutoSizeTextTypeUniformWithConfiguration(28, 72, 2, android.util.TypedValue.COMPLEX_UNIT_SP)
            maxLines = 1
            setPadding(dp(26), 0, dp(26), 0)
            // Updating each second must not repeatedly interrupt TalkBack.
            accessibilityLiveRegion = View.ACCESSIBILITY_LIVE_REGION_NONE
        }
        val dial = FrameLayout(this)
        ring = TimerRing(this)
        dial.addView(ring, FrameLayout.LayoutParams(-1, -1))
        dial.addView(clockView, FrameLayout.LayoutParams(-1, -1))
        root.addView(dial, LinearLayout.LayoutParams(-1, dp(244)).apply {
            topMargin = dp(16); bottomMargin = dp(16)
        })

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
                ViewGroup.LayoutParams.WRAP_CONTENT
            ).apply {
                topMargin = dp(18)
                bottomMargin = dp(8)
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
            LinearLayout.LayoutParams(0, -2, 1f).apply { marginEnd = dp(6) }
        )
        secondaryRow.addView(
            stopButton,
            LinearLayout.LayoutParams(0, -2, 1f).apply { marginStart = dp(6) }
        )
        root.addView(
            secondaryRow,
            LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT,
                ViewGroup.LayoutParams.WRAP_CONTENT
            )
        )

        rhythmView = label("40s rest · 20m focus", 14f, "#65766F", Typeface.NORMAL).apply {
            setPadding(0, dp(18), 0, dp(12))
        }
        root.addView(rhythmView)

        val settingsCard = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(dp(12), dp(12), dp(12), dp(12))
            background = roundedBackground("#FFFFFF", 22f, "#DCE9DF")
        }
        val optionsBody = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            visibility = if (optionsExpanded) View.VISIBLE else View.GONE
        }
        val optionsToggle = actionButton("Options  +", primary = false).apply {
            text = if (optionsExpanded) "Options  −" else "Options  +"
            minHeight = dp(48)
            setOnClickListener {
                optionsExpanded = !optionsExpanded
                optionsBody.visibility = if (optionsExpanded) View.VISIBLE else View.GONE
                text = if (optionsExpanded) "Options  −" else "Options  +"
                contentDescription = if (optionsExpanded) "Options, expanded" else "Options, collapsed"
            }
            contentDescription = if (optionsExpanded) "Options, expanded" else "Options, collapsed"
        }
        settingsCard.addView(optionsToggle, LinearLayout.LayoutParams(-1, -2))
        settingsCard.addView(optionsBody)

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
        optionsBody.addView(
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
        breakMusicCheck = CheckBox(this).apply {
            text = "Gentle music during breaks"
            textSize = 16f
            setTextColor(Color.parseColor("#40564D"))
            setOnCheckedChangeListener { _, _ -> settingsChanged() }
        }
        listOf(voiceCheck, chimeCheck, breakMusicCheck).forEach {
            it.minHeight = dp(48); optionsBody.addView(it)
        }
        optionsBody.addView(label(
            "A calm voice, ready offline. Music softens while it speaks. Duration changes apply to the next phase.",
            13f,
            "#52655B",
            Typeface.NORMAL
        ).apply {
            setLineSpacing(0f, 1.16f)
            setPadding(0, dp(8), 0, 0)
        })
        notificationNote = actionButton("Enable lock-screen controls", primary = false).apply {
            textSize = 14f
            minHeight = dp(48)
            setOnClickListener {
                startActivity(Intent(Settings.ACTION_APP_NOTIFICATION_SETTINGS)
                    .putExtra(Settings.EXTRA_APP_PACKAGE, packageName))
            }
        }
        optionsBody.addView(notificationNote)
        root.addView(
            settingsCard,
            LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT,
                ViewGroup.LayoutParams.WRAP_CONTENT
            ).apply { topMargin = dp(16) }
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
        clockView.contentDescription = "${snapshot.remainingSeconds / 60} minutes, ${snapshot.remainingSeconds % 60} seconds remaining"
        ring.progress = if (snapshot.totalSeconds > 0) 1f - snapshot.remainingSeconds.toFloat() / snapshot.totalSeconds else 0f
        ring.resting = snapshot.phase == TimerPhase.REST
        skipButton.contentDescription = if (snapshot.phase == TimerPhase.REST) "Skip eye rest and move to focus" else "Skip focus and move to eye rest"
        val prefs = AppSettings.load(this)
        rhythmView.text = "${prefs.restSeconds}s rest · ${prefs.workMinutes}m focus"
        primaryButton.text = when {
            snapshot.running -> "Pause"
            ready -> "Start timer"
            else -> "Resume"
        }
        detailView.text = when {
            ready -> "A little space for your eyes. Rest first, then focus."
            snapshot.phase == TimerPhase.REST && snapshot.running ->
                "Look far away and let your gaze soften. The audio will guide you back."
            snapshot.phase == TimerPhase.WORK && snapshot.running ->
                "Work quietly. The next eye rest starts automatically."
            else -> pauseReason.ifEmpty { "Take your time. Resume when you're ready." }
        }
        if (snapshot.running && Build.VERSION.SDK_INT >= 33 &&
            checkSelfPermission(Manifest.permission.POST_NOTIFICATIONS) != PackageManager.PERMISSION_GRANTED) {
            detailView.append(" Notifications are off; lock-screen controls are hidden.")
        }
    }

    private fun loadSettingsIntoUi() {
        loadingSettings = true
        val settings = AppSettings.load(this)
        restSecondsInput.setText(settings.restSeconds.toString())
        workMinutesInput.setText(settings.workMinutes.toString())
        voiceCheck.isChecked = settings.voiceEnabled
        chimeCheck.isChecked = settings.chimeEnabled
        breakMusicCheck.isChecked = settings.breakMusicEnabled
        loadingSettings = false
    }

    private fun settingsChanged() {
        if (loadingSettings) return
        saveSettingsFromUi()
        sendServiceAction(EyeRestService.ACTION_REFRESH_SETTINGS)
        if (!currentSnapshot.running && currentSnapshot.remainingSeconds == currentSnapshot.totalSeconds && currentSnapshot.completedRests == 0) {
            val seconds = if (currentSnapshot.phase == TimerPhase.REST) AppSettings.load(this).restSeconds else AppSettings.load(this).workMinutes * 60
            render(currentSnapshot.copy(remainingSeconds = seconds, totalSeconds = seconds))
        }
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
                chimeEnabled = chimeCheck.isChecked,
                breakMusicEnabled = breakMusicCheck.isChecked
            )
        )
        restSecondsInput.setText(saved.restSeconds.toString())
        workMinutesInput.setText(saved.workMinutes.toString())
        rhythmView.text = "${saved.restSeconds}s rest · ${saved.workMinutes}m focus"
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
            field.id = View.generateViewId()
            field.contentDescription = "$title. ${if (title.startsWith("Rest")) "5 to 300 seconds" else "1 to 180 minutes"}"
            addView(label(title, 13f, "#52655B", Typeface.NORMAL).apply { labelFor = field.id })
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
        maxLines = 1
        imeOptions = android.view.inputmethod.EditorInfo.IME_ACTION_DONE
        setOnEditorActionListener { _, action, _ ->
            if (action == android.view.inputmethod.EditorInfo.IME_ACTION_DONE) {
                clearFocus()
                getSystemService(android.view.inputmethod.InputMethodManager::class.java)
                    .hideSoftInputFromWindow(windowToken, 0)
                true
            } else false
        }
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
        minHeight = dp(if (primary) 64 else 48)
        setPadding(dp(16), dp(12), dp(16), dp(12))
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

# Eye Rest Android Prototype Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and publish a debug Android APK whose timer and spoken eye-rest cues continue while the phone is locked.

**Architecture:** A pure Kotlin timer state machine feeds a foreground Android service. The service owns timing, wake lock, notification actions, TTS/audio playback, persistence, and broadcasts state to a lightweight activity UI.

**Tech Stack:** Kotlin 2.0.21, Android Gradle Plugin 8.7.3, Gradle 8.10.2, Android SDK 35, JUnit 4, GitHub Actions.

## Global Constraints

- Minimum SDK is API 26.
- Compile and target SDK are API 35.
- Defaults are 40 seconds rest and 20 minutes work.
- The cycle starts with rest.
- Notification actions are Pause/Resume, Skip, and Stop.
- Voice and chimes are independently configurable.
- The active service holds a partial wake lock and releases it on pause or stop.
- No exact-alarm or reboot-start permission in the prototype.

---

### Task 1: Project scaffold and failing timer tests

**Files:**
- Create: `eye-rest-android/settings.gradle.kts`
- Create: `eye-rest-android/build.gradle.kts`
- Create: `eye-rest-android/app/build.gradle.kts`
- Create: `eye-rest-android/app/src/main/AndroidManifest.xml`
- Create: `eye-rest-android/app/src/main/res/values/strings.xml`
- Create: `eye-rest-android/app/src/main/res/values/themes.xml`
- Test: `eye-rest-android/app/src/test/java/com/wxyz/eyerest/TimerEngineTest.kt`
- Test: `eye-rest-android/app/src/test/java/com/wxyz/eyerest/FormattersTest.kt`

**Interfaces:**
- Produces: `TimerEngine`, `TimerConfig`, `TimerSnapshot`, `TimerEvent`, `formatDuration(seconds: Int)`, and `clampConfig(restSeconds: Int, workMinutes: Int)` expectations.

- [ ] **Step 1: Write failing tests** for initial state, pause/resume, transition, skip, guidance events, formatting, and clamping.
- [ ] **Step 2: Run `gradle testDebugUnitTest` in GitHub Actions.** Expected: compilation failure because the production classes do not exist.
- [ ] **Step 3: Record the failing workflow conclusion before adding implementation.**

### Task 2: Timer engine and formatting utilities

**Files:**
- Create: `eye-rest-android/app/src/main/java/com/wxyz/eyerest/TimerEngine.kt`
- Create: `eye-rest-android/app/src/main/java/com/wxyz/eyerest/Formatters.kt`

**Interfaces:**
- `TimerEngine(config: TimerConfig, nowMillis: () -> Long)`
- `fun start(): TickResult`
- `fun pause(): TimerSnapshot`
- `fun skip(): TickResult`
- `fun stop(): TimerSnapshot`
- `fun updateConfig(config: TimerConfig): TimerSnapshot`
- `fun tick(): TickResult`
- `fun snapshot(): TimerSnapshot`

- [ ] **Step 1: Implement the smallest absolute-time state machine that satisfies the tests.**
- [ ] **Step 2: Implement threshold crossing events for rest halfway, five seconds, and three-to-one countdown.**
- [ ] **Step 3: Run `gradle testDebugUnitTest`.** Expected: all unit tests pass.

### Task 3: Settings and state persistence

**Files:**
- Create: `eye-rest-android/app/src/main/java/com/wxyz/eyerest/AppSettings.kt`
- Create: `eye-rest-android/app/src/main/java/com/wxyz/eyerest/TimerStore.kt`

**Interfaces:**
- `AppSettings.load(context): UserSettings`
- `AppSettings.save(context, UserSettings)`
- `TimerStore.save(context, TimerSnapshot)`
- `TimerStore.load(context): TimerSnapshot?`

- [ ] **Step 1: Store rest seconds, work minutes, voice enabled, and chime enabled in `SharedPreferences`.**
- [ ] **Step 2: Store the latest timer snapshot for activity recreation and service status display.**
- [ ] **Step 3: Keep persistence primitive-only and tolerate missing or malformed values by returning defaults.**

### Task 4: Cached voice guidance

**Files:**
- Create: `eye-rest-android/app/src/main/java/com/wxyz/eyerest/VoiceGuide.kt`

**Interfaces:**
- `enum class VoicePrompt`
- `class VoiceGuide(context: Context)`
- `fun prepare()`
- `fun play(prompt: VoicePrompt, chime: Boolean)`
- `fun close()`

- [ ] **Step 1: Initialize `TextToSpeech`, choose an English voice, and set rate to 0.88.**
- [ ] **Step 2: Synthesize fixed prompts into cache files with stable IDs.**
- [ ] **Step 3: Prefer cached `MediaPlayer` playback; fall back to direct TTS.**
- [ ] **Step 4: Add a short `ToneGenerator` cue when chimes are enabled.**
- [ ] **Step 5: Release TTS, player, and tone resources in `close()`.**

### Task 5: Foreground timer service and notification controls

**Files:**
- Create: `eye-rest-android/app/src/main/java/com/wxyz/eyerest/EyeRestService.kt`

**Interfaces:**
- Actions: `ACTION_START_OR_RESUME`, `ACTION_PAUSE`, `ACTION_SKIP`, `ACTION_STOP`, `ACTION_REFRESH_SETTINGS`.
- Broadcast: `ACTION_STATE_CHANGED` with phase, running state, and remaining seconds.

- [ ] **Step 1: Create the notification channel and enter foreground state immediately on start.**
- [ ] **Step 2: Route service intents to timer-engine actions.**
- [ ] **Step 3: Run a 250 ms handler loop and update the notification only when the displayed second changes.**
- [ ] **Step 4: Map timer events to `VoicePrompt` playback.**
- [ ] **Step 5: Acquire a non-reference-counted partial wake lock while running; release on pause, stop, and destroy.**
- [ ] **Step 6: Build Pause/Resume, Skip, and Stop notification actions with immutable service `PendingIntent`s.**
- [ ] **Step 7: Persist and broadcast each visible state update.**

### Task 6: Activity UI and permissions

**Files:**
- Create: `eye-rest-android/app/src/main/java/com/wxyz/eyerest/MainActivity.kt`

**Interfaces:**
- Sends service actions through explicit intents.
- Receives `ACTION_STATE_CHANGED` broadcasts.

- [ ] **Step 1: Build a programmatic portrait-friendly UI with phase, countdown, Start/Pause, Skip, Stop, settings fields, and toggles.**
- [ ] **Step 2: Request `POST_NOTIFICATIONS` on API 33 and newer before starting.**
- [ ] **Step 3: Clamp and save settings, then send them to the service.**
- [ ] **Step 4: Register a non-exported receiver while visible and render stored state on resume.**
- [ ] **Step 5: Explain in the UI that the ongoing notification and wake lock enable locked-screen guidance.**

### Task 7: Continuous integration and APK artifact

**Files:**
- Create: `.github/workflows/eye-rest-android.yml`
- Create: `eye-rest-android/build-trigger.txt`
- Create: `eye-rest-android/README.md`

**Interfaces:**
- Workflow artifact name: `eye-rest-android-debug-apk`.

- [ ] **Step 1: Configure Actions to install Java 21, Android SDK 35, build tools 35.0.0, and Gradle 8.10.2.**
- [ ] **Step 2: Run `gradle testDebugUnitTest assembleDebug --stacktrace`.**
- [ ] **Step 3: Upload `app/build/outputs/apk/debug/app-debug.apk`.**
- [ ] **Step 4: Trigger the workflow after implementation and inspect the complete job result.**
- [ ] **Step 5: Download the artifact and verify the APK ZIP entry and SHA-256 checksum.**

### Task 8: Delivery review

**Files:**
- Review all files under `eye-rest-android/` and the workflow.

- [ ] **Step 1: Compare the implementation against every requirement in the design.**
- [ ] **Step 2: Confirm tests have zero failures and APK assembly exits successfully.**
- [ ] **Step 3: Prepare a decision log covering wake-lock battery tradeoff, cached TTS, lightweight UI, language, reboot behavior, and Play Store readiness.**

# Eye Rest Android Prototype Design

## Goal

Build a sideloadable Android APK that continues timing and spoken eye-rest guidance while the phone is locked. It complements the existing PWA rather than replacing it.

## Product behavior

- Default cycle: 40 seconds of rest, followed by 20 minutes of focus.
- The cycle starts with a rest period and repeats until stopped.
- Spoken cues continue with the display locked.
- The persistent notification shows the active phase and remaining time.
- Notification actions: Pause/Resume, Skip, and Stop.
- In-app controls mirror the notification controls.
- Rest and work duration are editable and persisted.
- Voice and chimes can be enabled independently.

## Architecture

### Native Android app

The prototype is a native Kotlin Android application. It intentionally avoids a WebView and Jetpack Compose for the first APK. A small programmatic Android UI reduces dependencies and keeps the reliability work concentrated in the foreground service.

### Timer engine

`TimerEngine` is a platform-independent state machine. It stores an absolute monotonic end time instead of decrementing a counter, preventing drift when callbacks arrive late. It emits semantic events for phase changes and rest guidance thresholds.

### Foreground service

`EyeRestService` owns the running session. While active it:

- runs as a foreground media-playback service;
- publishes an ongoing notification;
- holds a partial wake lock so the CPU remains available after screen lock;
- updates state from `SystemClock.elapsedRealtime()`;
- dispatches audio prompts and chimes;
- persists the latest snapshot for activity recreation.

The wake lock is released whenever the session is paused or stopped.

### Voice guidance

`VoiceGuide` initializes Android `TextToSpeech`, selects an English voice when available, and pre-generates fixed guidance phrases into the app cache. Playback prefers the cached files and falls back to direct TTS if generation or playback is unavailable.

Default phrases:

- Rest start: “Time for an eye break. Look far away and blink slowly.”
- Halfway: “Keep looking far away. Relax your eyes.”
- Five seconds: “Almost done. Five seconds.”
- Countdown: “Three.”, “Two.”, “One.”
- Work start: “Eye break complete. Back to work.”

### UI and settings

`MainActivity` provides a large phase label, countdown, primary start/pause control, skip and stop controls, duration fields, and voice/chime toggles. Settings are stored in `SharedPreferences` and sent to the service when a session starts or changes.

## Reliability choices

- Minimum Android version: Android 8.0 / API 26.
- Compile and target SDK: API 35.
- Foreground service type: `mediaPlayback`.
- The app requests notification permission on Android 13 and newer.
- A partial wake lock is used during active timing instead of exact-alarm permission. This favors predictable spoken cues at the cost of additional battery usage.
- Service state is sticky and stored locally, but the first prototype does not automatically resume after a device reboot.

## Error handling

- If notification permission is denied, the activity explains that locked-screen reliability is limited and offers another request.
- If TTS initialization fails, chimes still operate and the UI remains functional.
- If cached audio cannot be generated or played, direct TTS is attempted.
- Invalid duration input is clamped to 5–300 seconds for rest and 1–180 minutes for work.
- Service teardown releases wake lock, audio player, TTS, handlers, and foreground notification.

## Testing

Pure JVM tests cover:

- initial state and defaults;
- pause/resume without losing time;
- phase transitions based on absolute time;
- skip behavior;
- rest halfway, five-second, and countdown events;
- notification text formatting;
- duration clamping.

GitHub Actions runs unit tests and assembles a debug APK. The workflow uploads the APK as an artifact.

## Deferred decision points

- Direct TTS only versus cached prompts.
- Battery-saving exact alarms versus continuous partial wake lock.
- Compose redesign versus the lightweight native UI.
- English-only prompts versus selectable languages and custom scripts.
- Auto-start after reboot.
- Play Store packaging, signing, privacy disclosures, and foreground-service declarations.

# Eye Rest Android Prototype

Native Android companion for the Eye Rest PWA. It uses a foreground media service and partial wake lock so the timer, music, chimes, and spoken prompts can continue while the phone is locked.

## Current behavior

- 40-second rest and 20-minute work defaults
- Repeating rest/work cycle
- Prefers the highest-quality English natural, neural, premium, or network TTS voice installed on the phone
- Versioned speech cache so upgraded voices replace older robotic recordings
- Locally generated gentle ambient music during eye-rest periods
- Music automatically ducks while voice guidance speaks
- Persistent lock-screen notification
- Pause/Resume, Skip, and Stop notification actions
- Editable durations
- Independent voice, chime, and break-music toggles
- Android 8.0 / API 26 minimum

## Install the prototype

1. Download `app-debug.apk` from the `eye-rest-android-debug-apk` GitHub Actions artifact.
2. Open the APK on the Android phone.
3. Allow installation from the browser or file manager when Android asks.
4. Open **Eye Rest** and allow notifications.
5. Tap **Start timer**, then lock the phone.

The APK is debug-signed for personal sideload testing. It is not Play Store–ready.

## Voice quality

The app selects the best English voice reported by the phone's TTS engine. It strongly prefers voices whose names indicate natural, neural, WaveNet, studio, premium, or enhanced quality. A network voice may be selected when available, so the first prompt can benefit from an internet connection. The app falls back to the best locally installed voice.

Android voice quality still depends on the TTS engine and voice packages installed on the phone. On Pixel devices, keeping **Speech Services by Google** and its English voice data updated generally provides the best result.

## Break music

Break music is synthesized locally by the app as a quiet, slowly changing ambient chord progression. It requires no download or streaming, runs only during the rest phase, and becomes much quieter while a spoken prompt is active.

## Reliability notes

- An ongoing notification remains visible while the service is active.
- The app holds a partial wake lock only while the timer is running.
- Pause releases the wake lock and stops the music; Stop removes the notification and terminates the service.
- The first spoken prompt may use direct TTS while fixed prompts are being cached.
- The prototype does not automatically restart after a phone reboot.

## Build

The repository workflow installs Android SDK 35 and runs:

```bash
gradle testDebugUnitTest assembleDebug --stacktrace --no-daemon
```

The debug APK is produced at:

```text
app/build/outputs/apk/debug/app-debug.apk
```

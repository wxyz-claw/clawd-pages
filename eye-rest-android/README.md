# Eye Rest Android Prototype

Native Android companion for the Eye Rest PWA. It uses a foreground media service and partial wake lock so the timer, chimes, and spoken prompts can continue while the phone is locked.

## Current behavior

- 40-second rest and 20-minute work defaults
- Repeating rest/work cycle
- Cached Android text-to-speech prompts with direct-TTS fallback
- Persistent lock-screen notification
- Pause/Resume, Skip, and Stop notification actions
- Editable durations
- Independent voice and chime toggles
- Android 8.0 / API 26 minimum

## Install the prototype

1. Download `app-debug.apk` from the `eye-rest-android-debug-apk` GitHub Actions artifact.
2. Open the APK on the Android phone.
3. Allow installation from the browser or file manager when Android asks.
4. Open **Eye Rest** and allow notifications.
5. Tap **Start timer**, then lock the phone.

The APK is debug-signed for personal sideload testing. It is not Play Store–ready.

## Reliability notes

- An ongoing notification remains visible while the service is active.
- The app holds a partial wake lock only while the timer is running.
- Pause releases the wake lock; Stop removes the notification and terminates the service.
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

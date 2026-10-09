# Eye Rest for Android — 0.3.0 review candidate

A small native companion for the Eye Rest PWA. Start with 40 seconds away from your screen, then 20 minutes of focus. The cycle repeats until you stop it. Timing and audio use the original foreground media service and partial wake lock for screen-off operation.

## This update

- Four bundled, short English narration clips use the approved Heart voice, generated offline with Kokoro. Normal speech needs neither a network nor a device TTS engine. Android offline TTS remains a playback-error fallback.
- Guidance leaves room for silence. The last three seconds use optional quiet chimes, rather than cutting off spoken countdown numbers.
- Pause, Stop, Skip, voice-off, interrupted audio focus, and headphone disconnection cancel sound. Old decoder callbacks cannot affect the next prompt. Focus denial pauses with an explanation; resuming is explicit.
- Optional local ambient music plays only during rest, fades in, and ducks while speech plays.
- A pale mint screen, leaf mark, circular progress dial and one primary action preserve the minimalist direction. Options begin collapsed; there are no test-voice or diagnostic controls.
- Controls have 48dp minimum targets, phase changes announce politely, the ticking clock does not repeatedly interrupt TalkBack, and the screen scrolls at large font sizes. System-bar insets and rotation are supported.
- Existing settings keys and app identity are preserved. Loading an activity no longer overwrites independent audio preferences. Duration changes apply to the next phase.
- Monotonic deadlines survive service recreation on the same boot. A reboot never resumes a saved active session. Late callbacks use current cues instead of replaying expired phases.

## Personal sideload testing

The existing GitHub Actions workflow builds a debug APK and retains test/lint reports and native view renders. This is a review candidate, not a store release. Device-specific screen-off behavior, calls/Bluetooth routing, listening quality and TalkBack still require physical-device evaluation; simulated tests are labeled separately in `QUALITY.md`.

**Keep the installed app and its data.** A debug APK can update it only if its signing certificate matches the installed APK. The original workflow generated ephemeral debug keys; this checkout contains no recoverable old signing key. Do not uninstall or clear data to bypass a signature mismatch. Compare signing certificates before upgrading, and use the original signing key if it becomes available.

Android 8.0/API26 minimum, target/compile SDK35. English only. No reboot auto-start, account, paid voice service, analytics or new Android permissions.

## Audio provenance

See `third-party/narration-provenance.json` for text, hashes and durations, and `third-party/Kokoro-APACHE-2.0.txt` for license attribution. The app bundles WAV clips, not a synthesis model/runtime. [Official Kokoro-82M model](https://huggingface.co/hexgrad/Kokoro-82M), fixed revision `f3ff3571791e39611d31c381e3a41a3af07b4987`, voice `af_heart`, speed0.94. Total bundled PCM is about507KB. Naturalness is a listening judgment; successful generation/decode does not certify it.

## Build

Use the original pinned Gradle8.10.2, Java21 and Android SDK35 toolchain:

```sh
gradle testDebugUnitTest lintDebug assembleDebug --stacktrace --no-daemon
```

APK: `app/build/outputs/apk/debug/app-debug.apk`. The existing public GitHub workflow can provide this toolchain without installing an SDK or emulator on the user's Mac.

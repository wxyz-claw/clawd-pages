# Review and acceptance evidence

Baseline recovered from draftPR1 commit dc8d0b7760d1af5e3c0f7f219d1110ac9b9cc601. The user's existing main checkout, digest changes, podcast source/runtime/feed and existing installed app are untouched.

## Automated coverage

Pure timer tests: defaults, absolute-time phase transitions, pause/resume, skip, delayed callbacks, current-only countdown, same-boot deadline recreation, next-phase settings and stop. Formatting tests retain the original coverage.

Android simulation tests run against API26 and API35: old independent audio preference loading, collapsed options, packaged voice playback without TTS, cancellation and stale completion callbacks, silent/countdown paths, Pause wake-lock release, focus denial, focus loss, noisy-route broadcast, sticky restart after pause, same-boot state and reboot behavior. Native graphics renders capture the actual activity views at 100% and200% font scale; these are simulated Android renders, not device screenshots. Lint and APK assembly use the original CI toolchain.

## Locally verified

- Four WAV recordings generated offline with the existing installed Kokoro runtime and fixed local model/voice assets. No dependency/model installation or podcast mutation.
- Every WAV fully decodes with FFmpeg, mono24kHz, nonzero PCM, no clipping. Hashes and durations in third-party/narration-provenance.json. Each phrase fits its allotted cue window.
- The baseline contains no applicable AGENTS.md/.agents instructions. Changes are isolated to Eye Rest source/docs and its Android build workflow.

## Physical-device gates still open

- Listen to each clip and the complete40-second break, with music/chimes on/off, and judge warmth, clarity and comfort.
- Start, lock the display, cross rest→focus→rest; repeat with battery saver and app recreation. Check no duplicated or stale speech.
- Pause/Resume, Skip and Stop from both app and lock-screen controls; verify idle/pause has no audio or held wake lock.
- Calls, competing playback, focus denial, wired/Bluetooth disconnection/reconnection; verify explicit resume and safe speaker behavior.
- Notification permission denied/revoked, device restart, airplane mode, missing TTS engine and failed playback fallback.
- TalkBack focus, large text, compact screens, rotation, keyboard editing and visible action targets.
- Existing APK certificate matching before data-preserving upgrade. Never uninstall or clear data to work around signing.

No physical Android device or Android SDK/emulator is installed on this Mac. Existing remote CI can build and simulate; it cannot establish device audio naturalness or OEM screen-off behavior. This update is a review candidate until the device gates pass.

# Eye Rest Preview — separate app and settings

The `preview` build type uses the same improved timer/audio code with application ID `com.wxyz.eyerest.preview` and display name **Eye Rest Preview**. Android gives it a separate app sandbox, settings, timer state and notification channel. It does not update the original `com.wxyz.eyerest` app or import its data. The preview screen persistently labels its separate settings. No main activity, service, storage or permission source was modified to add this variant; labeling exists only in preview sources/resources.

Normal debug/release application ID, version, signing configuration and release configuration remain unchanged. The preview inherits the existing debug build configuration; it is a reversible additional build type rather than a replacement project.

Build with the existing toolchain:

```sh
gradle testPreviewUnitTest lintPreview assemblePreview --stacktrace --no-daemon
```

APK: `app/build/outputs/apk/preview/app-preview.apk`. Normal APK remains at `app/build/outputs/apk/debug/app-debug.apk`.

## Evaluation limits

The verified preview may be manually sideloaded as an additional app on Android8/API26 or later if the device permits debug APKs. No phone installation or permission-settings change was performed. Keep the original app and its data. The normal candidate APK still cannot update the originally delivered APK because its signing key differs.

Preview settings and timer history start separately. Evaluate one active timer at a time because both apps request media audio focus. Physical-device listening, locked-screen/OEM behavior, notification permission, routes, TalkBack and keyboard/insets remain unverified. The preview uses an ephemeral CI debug signing certificate; a future preview APK requires a matching certificate to update this preview in place. No stable signing credentials were added.

CI verifies both application IDs and labels, no sharedUserId, equal existing permission sets, signature and ZIP integrity, normal and preview unit/lifecycle tests, native renders and lint. Source/normal APK content comparisons establish that adding the variant did not change normal production files or compiled payload.

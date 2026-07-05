# 20-20-20 Eye Rest Timer PWA

A small eye-rest timer with voice guidance, chimes, and screen-awake modes.

## Defaults

- Rest: 40 seconds
- Work: 20 minutes
- Screen awake: Reliable + dim screen

## Why HTTPS/PWA matters

Opening the app as a downloaded `file://` page in Chrome is not reliable for keeping the screen awake. Chrome generally needs a secure context, such as HTTPS or an installed PWA, for Screen Wake Lock.

Also, a web page cannot reliably wake a fully sleeping phone after 20 minutes. Reliable mode works by keeping the page awake and dimming the screen during the work block.

## Recommended mobile setup

1. Open the hosted page in Chrome.
2. Chrome menu → **Add to Home screen** or **Install app**.
3. Launch it from the home screen.
4. Tap **Start**.
5. Keep **Screen awake** set to **Reliable + dim screen**.

## Expected GitHub Pages URL

If GitHub Pages is enabled for this repo from the `main` branch/root, the app should be available at:

https://wxyz-claw.github.io/clawd-pages/eye-rest/

## Limitation

Voice quality depends on the voices installed in the browser/device. For true locked-screen alarms without keeping the page awake, use a native app or OS-level alarm/notification system.

package com.wxyz.eyerest

import android.content.Context
import android.content.Intent
import android.graphics.Bitmap
import android.graphics.Canvas
import android.media.AudioManager
import android.media.MediaPlayer
import android.os.Looper
import android.os.PowerManager
import android.provider.Settings
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.CheckBox
import android.widget.ScrollView
import org.junit.Assert.*
import org.junit.Before
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.Robolectric
import org.robolectric.RobolectricTestRunner
import org.robolectric.RuntimeEnvironment
import org.robolectric.Shadows.shadowOf
import org.robolectric.annotation.Config
import org.robolectric.annotation.GraphicsMode
import org.robolectric.shadows.ShadowMediaPlayer
import org.robolectric.util.ReflectionHelpers
import java.io.File

@RunWith(RobolectricTestRunner::class)
@Config(sdk = [26, 35], qualifiers = "w360dp-h800dp-mdpi")
class AppExperienceTest {
    private val context get() = RuntimeEnvironment.getApplication()

    @Before fun prepare() {
        context.getSharedPreferences("eye_rest_settings", Context.MODE_PRIVATE).edit().clear().commit()
        context.getSharedPreferences("eye_rest_timer_state", Context.MODE_PRIVATE).edit().clear().commit()
        Settings.Global.putInt(context.contentResolver, Settings.Global.BOOT_COUNT, 10)
        ShadowMediaPlayer.setMediaInfoProvider { ShadowMediaPlayer.MediaInfo(3_000, -1) }
    }

    @Test fun oldSettingsSurviveActivityLoadingAndOptionsStartCollapsed() {
        val original = UserSettings(55, 12, false, true, false)
        AppSettings.save(context, original)
        val controller = Robolectric.buildActivity(MainActivity::class.java).setup()
        val activity = controller.get()
        assertEquals(original, AppSettings.load(context))
        val all = descendants(activity.window.decorView)
        val voice = all.filterIsInstance<CheckBox>().first { it.text == "Voice guidance" }
        assertFalse(voice.isShown)
        all.filterIsInstance<Button>().first { it.text == "Options  +" }.performClick()
        assertTrue(voice.isShown)
        controller.pause().stop().destroy()
        assertEquals(original, AppSettings.load(context))
    }

    @Test fun bundledVoiceNeedsNoTtsAndStaleCompletionCannotUnduckNewSpeech() {
        val states = mutableListOf<Boolean>()
        val guide = VoiceGuide(context) { states += it }
        guide.play(VoicePrompt.REST_START, true, false)
        val first = ReflectionHelpers.getField<MediaPlayer>(guide, "player")
        assertNull(ReflectionHelpers.getField<Any?>(guide, "tts"))
        guide.play(VoicePrompt.HALFWAY, true, false)
        assertTrue(states.last())
        val count = states.size
        shadowOf(first).invokeCompletionListener()
        assertEquals(count, states.size)
        guide.cancel()
        assertFalse(states.last())
        guide.close()
    }

    @Test fun voiceOffAndCountdownNeverStartNarration() {
        val guide = VoiceGuide(context)
        guide.play(VoicePrompt.REST_START, false, false)
        assertNull(ReflectionHelpers.getField<Any?>(guide, "player"))
        guide.play(VoicePrompt.THREE, true, false)
        assertNull(ReflectionHelpers.getField<Any?>(guide, "player"))
        guide.close()
    }

    @Test fun pauseStopsSpeechAndReleasesWakeLock() {
        AppSettings.save(context, UserSettings(breakMusicEnabled = false, chimeEnabled = false))
        val controller = Robolectric.buildService(EyeRestService::class.java).create()
        val service = controller.get()
        service.onStartCommand(EyeRestService.intent(service, EyeRestService.ACTION_START_OR_RESUME), 0, 1)
        val guide = ReflectionHelpers.getField<VoiceGuide>(service, "voiceGuide")
        assertNotNull(ReflectionHelpers.getField<Any?>(guide, "player"))
        val music = ReflectionHelpers.getField<BreakMusicPlayer>(service, "breakMusicPlayer")
        assertTrue(ReflectionHelpers.getField<Boolean>(music, "ducked"))
        service.onStartCommand(EyeRestService.intent(service, EyeRestService.ACTION_PAUSE), 0, 2)
        assertNull(ReflectionHelpers.getField<Any?>(guide, "player"))
        assertFalse(ReflectionHelpers.getField<Boolean>(music, "ducked"))
        assertFalse(ReflectionHelpers.getField<PowerManager.WakeLock>(service, "wakeLock").isHeld)
        assertFalse(TimerStore.load(context)!!.running)
        controller.destroy()
    }

    @Test fun switchingVoiceOffCancelsCurrentSpeechWithoutStoppingTimer() {
        AppSettings.save(context, UserSettings(breakMusicEnabled = false, chimeEnabled = false))
        val controller = Robolectric.buildService(EyeRestService::class.java).create()
        val service = controller.get()
        service.onStartCommand(EyeRestService.intent(service, EyeRestService.ACTION_START_OR_RESUME), 0, 1)
        AppSettings.save(context, UserSettings(voiceEnabled = false, breakMusicEnabled = false, chimeEnabled = false))
        service.onStartCommand(EyeRestService.intent(service, EyeRestService.ACTION_REFRESH_SETTINGS), 0, 2)
        val guide = ReflectionHelpers.getField<VoiceGuide>(service, "voiceGuide")
        assertNull(ReflectionHelpers.getField<Any?>(guide, "player"))
        assertTrue(TimerStore.load(context)!!.running)
        controller.destroy()
    }

    @Test fun deniedAudioFocusPausesInsteadOfPlayingWithoutFocus() {
        AppSettings.save(context, UserSettings(breakMusicEnabled = false, chimeEnabled = false))
        val controller = Robolectric.buildService(EyeRestService::class.java).create()
        val service = controller.get()
        shadowOf(service.getSystemService(AudioManager::class.java)).setNextFocusRequestResponse(AudioManager.AUDIOFOCUS_REQUEST_FAILED)
        service.onStartCommand(EyeRestService.intent(service, EyeRestService.ACTION_START_OR_RESUME), 0, 1)
        shadowOf(Looper.getMainLooper()).idle()
        assertFalse(TimerStore.load(context)!!.running)
        assertFalse(ReflectionHelpers.getField<PowerManager.WakeLock>(service, "wakeLock").isHeld)
        controller.destroy()
    }

    @Test fun interruptionAndHeadphoneDisconnectPauseWithoutAutomaticResume() {
        AppSettings.save(context, UserSettings(breakMusicEnabled = false, chimeEnabled = false))
        val controller = Robolectric.buildService(EyeRestService::class.java).create()
        val service = controller.get()
        service.onStartCommand(EyeRestService.intent(service, EyeRestService.ACTION_START_OR_RESUME), 0, 1)
        val audio = shadowOf(service.getSystemService(AudioManager::class.java))
        audio.lastAudioFocusRequest.listener.onAudioFocusChange(AudioManager.AUDIOFOCUS_LOSS_TRANSIENT)
        assertFalse(TimerStore.load(context)!!.running)
        service.onStartCommand(EyeRestService.intent(service, EyeRestService.ACTION_START_OR_RESUME), 0, 2)
        service.sendBroadcast(Intent(AudioManager.ACTION_AUDIO_BECOMING_NOISY))
        shadowOf(Looper.getMainLooper()).idle()
        assertFalse(TimerStore.load(context)!!.running)
        assertEquals(android.app.Service.START_NOT_STICKY, service.onStartCommand(null, 0, 3))
        controller.destroy()
    }

    @Test fun rebootNeverRestoresRunningStateAndDeadlineIsPreservedOnSameBoot() {
        val original = TimerSnapshot(TimerPhase.REST, true, 30, 40, 0, 50_000)
        TimerStore.save(context, original)
        assertEquals(original, TimerStore.load(context))
        Settings.Global.putInt(context.contentResolver, Settings.Global.BOOT_COUNT, 11)
        assertFalse(TimerStore.load(context)!!.running)
    }

    @Test @Config(sdk = [35]) @GraphicsMode(GraphicsMode.Mode.NATIVE)
    fun renderActualNativeViewsAtNormalAndLargeTextSizes() {
        listOf(1f, 2f).forEach { scale ->
            RuntimeEnvironment.setFontScale(scale)
            val controller = Robolectric.buildActivity(MainActivity::class.java).setup()
            val view = controller.get().window.decorView
            view.measure(View.MeasureSpec.makeMeasureSpec(360, View.MeasureSpec.EXACTLY),
                View.MeasureSpec.makeMeasureSpec(800, View.MeasureSpec.EXACTLY))
            view.layout(0, 0, 360, 800)
            val image = Bitmap.createBitmap(360, 800, Bitmap.Config.ARGB_8888)
            view.draw(Canvas(image))
            val file = File("build/screenshots/ready-${scale}.png").apply { parentFile.mkdirs() }
            file.outputStream().use { image.compress(Bitmap.CompressFormat.PNG, 100, it) }
            assertTrue(file.length() > 1_000)
            assertTrue(descendants(view).filterIsInstance<Button>().first { it.text == "Start timer" }.height >= 48)
            descendants(view).filterIsInstance<Button>().first { it.text == "Options  +" }.performClick()
            view.measure(View.MeasureSpec.makeMeasureSpec(360, View.MeasureSpec.EXACTLY),
                View.MeasureSpec.makeMeasureSpec(800, View.MeasureSpec.EXACTLY))
            view.layout(0, 0, 360, 800)
            val scroll = descendants(view).filterIsInstance<ScrollView>().single()
            scroll.scrollTo(0, scroll.getChildAt(0).height)
            val optionsImage = Bitmap.createBitmap(360, 800, Bitmap.Config.ARGB_8888)
            view.draw(Canvas(optionsImage))
            File("build/screenshots/options-${scale}.png").outputStream().use {
                optionsImage.compress(Bitmap.CompressFormat.PNG, 100, it)
            }
            assertTrue(descendants(view).filterIsInstance<CheckBox>().all { it.height >= 48 })
            controller.pause().stop().destroy()
        }
        RuntimeEnvironment.setFontScale(1f)
    }

    private fun descendants(view: View): List<View> = listOf(view) +
        if (view is ViewGroup) (0 until view.childCount).flatMap { descendants(view.getChildAt(it)) } else emptyList()
}

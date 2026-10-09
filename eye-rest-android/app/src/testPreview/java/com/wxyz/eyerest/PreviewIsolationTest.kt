package com.wxyz.eyerest

import android.content.Context
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.Robolectric
import org.robolectric.RobolectricTestRunner
import org.robolectric.RuntimeEnvironment
import org.robolectric.annotation.Config

@RunWith(RobolectricTestRunner::class)
@Config(sdk = [26, 35], qualifiers = "w360dp-h800dp-mdpi")
class PreviewIsolationTest {
    @Test fun previewIdentityAndPersistentScopeLabelAreDistinct() {
        val context = RuntimeEnvironment.getApplication()
        assertEquals("com.wxyz.eyerest.preview", context.packageName)
        assertTrue(context is PreviewApplication)
        assertEquals("Eye Rest Preview", context.getString(R.string.app_name))
        val controller = Robolectric.buildActivity(MainActivity::class.java).setup()
        fun labels() = descendants(controller.get().window.decorView).filterIsInstance<TextView>().map { it.text.toString() }
        assertTrue("Eye Rest Preview" in labels())
        assertEquals(1, labels().count { it == "Preview · Separate settings and timer data" })
        controller.pause().resume()
        assertEquals(1, labels().count { it == "Preview · Separate settings and timer data" })
        controller.pause().stop().destroy()
    }

    @Test fun previewStorageAndServiceIntentsStayInItsOwnPackage() {
        val context = RuntimeEnvironment.getApplication()
        context.getSharedPreferences("eye_rest_settings", Context.MODE_PRIVATE).edit().clear().commit()
        assertTrue(context.dataDir.path.contains(context.packageName))
        AppSettings.save(context, UserSettings(restSeconds = 55, voiceEnabled = false))
        assertEquals(55, AppSettings.load(context).restSeconds)
        val intent = EyeRestService.intent(context, EyeRestService.ACTION_START_OR_RESUME)
        assertEquals("com.wxyz.eyerest.preview", intent.component!!.packageName)
        assertEquals("com.wxyz.eyerest.EyeRestService", intent.component!!.className)
    }

    private fun descendants(view: View): List<View> = listOf(view) +
        if (view is ViewGroup) (0 until view.childCount).flatMap { descendants(view.getChildAt(it)) }
        else emptyList()
}

package com.wxyz.eyerest

import android.graphics.Bitmap
import android.graphics.Canvas
import android.view.View
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.Robolectric
import org.robolectric.RobolectricTestRunner
import org.robolectric.annotation.Config
import org.robolectric.annotation.GraphicsMode
import java.io.File

/** CI-only renderer copied into the unchanged pinned prototype during baseline verification. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk = [35], qualifiers = "w360dp-h800dp-mdpi")
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class BaselineRenderTest {
    @Test fun renderOriginalActivity() {
        val controller = Robolectric.buildActivity(MainActivity::class.java).setup()
        val view = controller.get().window.decorView
        view.measure(View.MeasureSpec.makeMeasureSpec(360, View.MeasureSpec.EXACTLY),
            View.MeasureSpec.makeMeasureSpec(800, View.MeasureSpec.EXACTLY))
        view.layout(0, 0, 360, 800)
        view.viewTreeObserver.dispatchOnPreDraw()
        val image = Bitmap.createBitmap(360, 800, Bitmap.Config.ARGB_8888)
        view.draw(Canvas(image))
        val file = File("build/screenshots/original-ready-1.0.png").apply { parentFile.mkdirs() }
        file.outputStream().use { image.compress(Bitmap.CompressFormat.PNG, 100, it) }
        controller.pause().stop().destroy()
    }
}

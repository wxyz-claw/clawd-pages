package com.wxyz.eyerest

import android.content.Context
import android.graphics.Canvas
import android.graphics.Color
import android.graphics.Paint
import android.graphics.RectF
import android.view.View

/** Decorative progress ring; the accessible clock supplies the meaningful state. */
class TimerRing(context: Context) : View(context) {
    var progress = 0f
        set(value) { field = value.coerceIn(0f, 1f); invalidate() }
    var resting = true
        set(value) { field = value; invalidate() }
    private val paint = Paint(Paint.ANTI_ALIAS_FLAG).apply {
        style = Paint.Style.STROKE
        strokeWidth = 7 * resources.displayMetrics.density
        strokeCap = Paint.Cap.ROUND
    }
    init { importantForAccessibility = IMPORTANT_FOR_ACCESSIBILITY_NO }
    override fun onDraw(canvas: Canvas) {
        super.onDraw(canvas)
        val size = minOf(width, height).toFloat() - paint.strokeWidth * 2
        val bounds = RectF((width-size)/2, (height-size)/2, (width+size)/2, (height+size)/2)
        paint.color = Color.parseColor("#DCE8DF")
        canvas.drawOval(bounds, paint)
        paint.color = Color.parseColor(if (resting) "#4C876D" else "#6F8D82")
        canvas.drawArc(bounds, -90f, 360f * progress, false, paint)
    }
}

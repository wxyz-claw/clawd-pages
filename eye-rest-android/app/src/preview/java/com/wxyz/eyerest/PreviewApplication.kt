package com.wxyz.eyerest

import android.app.Activity
import android.app.Application
import android.graphics.Color
import android.os.Bundle
import android.view.Gravity
import android.view.View
import android.view.ViewGroup
import android.widget.LinearLayout
import android.widget.TextView

/** Preview-only labeling; the normal activity, service and storage code remain untouched. */
class PreviewApplication : Application() {
    override fun onCreate() {
        super.onCreate()
        registerActivityLifecycleCallbacks(object : ActivityLifecycleCallbacks {
            override fun onActivityResumed(activity: Activity) {
                if (activity !is MainActivity) return
                val heading = descendants(activity.window.decorView)
                    .filterIsInstance<TextView>().firstOrNull { it.text == "Eye Rest" } ?: return
                val parent = heading.parent as? LinearLayout ?: return
                heading.text = getString(R.string.app_name)
                val note = TextView(activity).apply {
                    text = getString(R.string.preview_scope_note)
                    textSize = 14f
                    gravity = Gravity.CENTER
                    setTextColor(Color.parseColor("#52655B"))
                }
                parent.addView(note, parent.indexOfChild(heading) + 1,
                    LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT,
                        ViewGroup.LayoutParams.WRAP_CONTENT).apply {
                        topMargin = (8 * resources.displayMetrics.density).toInt()
                    })
            }
            override fun onActivityCreated(activity: Activity, state: Bundle?) = Unit
            override fun onActivityStarted(activity: Activity) = Unit
            override fun onActivityPaused(activity: Activity) = Unit
            override fun onActivityStopped(activity: Activity) = Unit
            override fun onActivitySaveInstanceState(activity: Activity, state: Bundle) = Unit
            override fun onActivityDestroyed(activity: Activity) = Unit
        })
    }

    private fun descendants(view: View): List<View> = listOf(view) +
        if (view is ViewGroup) (0 until view.childCount).flatMap { descendants(view.getChildAt(it)) }
        else emptyList()
}

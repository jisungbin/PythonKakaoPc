package me.sungbin.pythonkakaopcwrapper.util

import android.app.Activity
import android.content.Context
import android.content.Intent
import androidx.core.net.toUri
import kotlin.random.Random
import kotlin.random.nextInt

object Util {
    private const val WearOsPackage = "com.google.android.wearable.app"

    fun checkWearInstalled(context: Context): Boolean {
        val result = context.packageManager.getLaunchIntentForPackage(WearOsPackage)
        return result != null
    }

    fun installWear(activity: Activity) {
        val intent = Intent(Intent.ACTION_VIEW)
        intent.addCategory(Intent.CATEGORY_DEFAULT)
        intent.data = "market://details?id=$WearOsPackage".toUri()
        activity.startActivity(intent)
    }

    fun generateDeviceUuid() = Random.nextInt(1000..10000)
}

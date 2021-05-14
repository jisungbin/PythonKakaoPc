package me.sungbin.pythonkakaopcwrapper.util

import android.app.Activity
import android.widget.Toast

/**
 * Created by SungBin on 5/15/21.
 */

fun Activity.toast(message: String) {
    Toast.makeText(applicationContext, message, Toast.LENGTH_SHORT).show()
}

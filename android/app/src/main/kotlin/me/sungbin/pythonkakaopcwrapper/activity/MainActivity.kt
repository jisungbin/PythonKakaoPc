package me.sungbin.pythonkakaopcwrapper.activity

import android.os.Bundle
import android.view.View
import androidx.appcompat.app.AppCompatActivity
import androidx.databinding.DataBindingUtil
import com.google.firebase.database.ktx.database
import com.google.firebase.ktx.Firebase
import me.sungbin.kakaotalkbotbasemodule.library.KakaoBot
import me.sungbin.pythonkakaopcwrapper.R
import me.sungbin.pythonkakaopcwrapper.databinding.ActivityMainBinding
import me.sungbin.pythonkakaopcwrapper.util.Util
import me.sungbin.pythonkakaopcwrapper.util.toast

class MainActivity : AppCompatActivity() {

    private lateinit var binding: ActivityMainBinding
    private val db = Firebase.database
    private val bot by lazy { KakaoBot().init(applicationContext) }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = DataBindingUtil.setContentView(this, R.layout.activity_main)

        kakaoSetup()
        checkRequirement()

        binding.btnRefreshRequirement.setOnClickListener {
            checkRequirement()
            toast(getString(R.string.main_toast_done_refresh))
        }
        binding.tvDeviceNumber.text = Util.generateDeviceUuid().toString()
    }

    private fun kakaoSetup() {
        bot.setMessageReceiveListener { sender, message, room, isGroupChat, action, profileImage, packageName, bot ->
            db.getReference("receive").child(room).push().setValue("{\nmessage: $message,\nroom: $room\n}")
        }
    }

    private fun checkRequirement() {
        binding.btnInstallWear.run {
            if (Util.checkWearInstalled(applicationContext)) {
                visibility = View.INVISIBLE
            } else {
                visibility = View.VISIBLE
                setOnClickListener {
                    Util.installWear(this@MainActivity)
                }
            }
        }

        binding.btnRequestNotificationPermission.run {
            if (bot.checkNotificationPermission()) {
                visibility = View.INVISIBLE
            } else {
                visibility = View.VISIBLE
                setOnClickListener {
                    bot.requestReadNotification()
                }
            }
        }
    }
}

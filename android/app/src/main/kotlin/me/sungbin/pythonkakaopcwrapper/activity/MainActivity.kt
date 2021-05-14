package me.sungbin.pythonkakaopcwrapper.activity

import android.os.Bundle
import android.view.View
import androidx.appcompat.app.AppCompatActivity
import androidx.databinding.DataBindingUtil
import com.google.firebase.database.DataSnapshot
import com.google.firebase.database.DatabaseError
import com.google.firebase.database.ValueEventListener
import com.google.firebase.database.ktx.database
import com.google.firebase.ktx.Firebase
import me.sungbin.kakaotalkbotbasemodule.library.KakaoBot
import me.sungbin.pythonkakaopcwrapper.R
import me.sungbin.pythonkakaopcwrapper.databinding.ActivityMainBinding
import me.sungbin.pythonkakaopcwrapper.util.Util
import me.sungbin.pythonkakaopcwrapper.util.toast

class MainActivity : AppCompatActivity() {

    private val uuid = Util.generateDeviceUuid().toString()
    private lateinit var binding: ActivityMainBinding
    private val db = Firebase.database
    private val bot by lazy { KakaoBot().init(applicationContext) }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = DataBindingUtil.setContentView(this, R.layout.activity_main)

        kakaoSetup()
        dbSetup()
        checkRequirement()

        binding.btnRefreshRequirement.setOnClickListener {
            checkRequirement()
            toast(getString(R.string.main_toast_done_refresh))
        }
        binding.tvDeviceNumber.text = uuid
    }

    private fun dbSetup() {
        db.getReference(uuid).child("status").addValueEventListener(object : ValueEventListener {
            override fun onDataChange(snapshot: DataSnapshot) {
                if (snapshot.value.toString().contains("connected")) {
                    binding.tvStatus.post {
                        binding.tvStatus.text = getString(R.string.main_label_python_status_done)
                    }
                }
            }

            override fun onCancelled(error: DatabaseError) {}
        })
    }

    private fun kakaoSetup() {
        bot.setMessageReceiveListener { sender, message, room, _, _, _, _, _ ->
            db.getReference(uuid).child("receive").child(room)
                .push().setValue("{ \"sender\": \"$sender\", \"message\": \"$message\" }")
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

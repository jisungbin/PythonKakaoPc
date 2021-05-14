package me.sungbin.pythonkakaopcwrapper.activity

import android.os.Bundle
import android.view.View
import androidx.appcompat.app.AppCompatActivity
import androidx.databinding.DataBindingUtil
import me.sungbin.pythonkakaopcwrapper.R
import me.sungbin.pythonkakaopcwrapper.databinding.ActivityMainBinding
import me.sungbin.pythonkakaopcwrapper.util.Util
import me.sungbin.pythonkakaopcwrapper.util.toast

class MainActivity : AppCompatActivity() {

    private lateinit var binding: ActivityMainBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = DataBindingUtil.setContentView(this, R.layout.activity_main)
        toast(Util.checkWearInstalled(applicationContext).toString())

        binding.btnInstallWear.run {
            if (Util.checkWearInstalled(applicationContext)) {
                visibility = View.INVISIBLE
            } else {
                setOnClickListener {
                    Util.installWear(this@MainActivity)
                }
            }
        }

        binding.tvDeviceNumber.text = Util.generateDeviceUuid().toString()
    }
}

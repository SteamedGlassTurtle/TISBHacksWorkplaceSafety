// main.kotlin.jerome.Action.kt

package main.kotlin.jerome

import android.content.Context
import android.media.MediaPlayer
import android.os.Handler
import android.util.Log
import android.widget.Toast
import android.content.Intent
import android.net.Uri

class Action(private val context: Context) {
    private var mediaPlayer: MediaPlayer? = null
    private val handler = Handler()
    private var isRunning = false

    private val runnable = Runnable {
        if (isRunning) {
            callEmergencyServices()
        }
    }

    fun startAction() {
        if (isRunning) return

        isRunning = true
        playSound()
        handler.postDelayed(runnable, 120000) // 2 minutes is the time when cpr intervention is most effective, so emergency is called after 2 minutes
    }

    private fun playSound() {
        mediaPlayer = MediaPlayer.create(context, R.raw.alarm_sound)
        mediaPlayer?.isLooping = true
        mediaPlayer?.start()
    }

    fun stopAction() {
        if (!isRunning) return

        isRunning = false
        mediaPlayer?.stop()
        mediaPlayer?.release()
        mediaPlayer = null
        handler.removeCallbacks(runnable)
    }

    fun onWatchTouched() {
        stopAction()
        Toast.makeText(context, "Action stopped.", Toast.LENGTH_SHORT).show()
    }

    private fun callEmergencyServices() {
        Log.d("Action", "Calling emergency services...")
        val intent = Intent(Intent.ACTION_DIAL)
        intent.data = Uri.parse("tel:112")
        intent.flags = Intent.FLAG_ACTIVITY_NEW_TASK
        context.startActivity(intent)
    }
}
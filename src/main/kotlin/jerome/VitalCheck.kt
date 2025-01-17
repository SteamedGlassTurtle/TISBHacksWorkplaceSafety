package main.kotlin.jerome

import android.hardware.Sensor
import android.hardware.SensorEvent
import android.hardware.SensorEventListener
import android.hardware.SensorManager
import android.os.Bundle
import android.util.Log
import com.google.android.gms.wearable.HealthServices
import com.google.android.gms.wearable.HealthServicesClient
import com.google.android.gms.wearable.Wearable
import kotlinx.coroutines.*

class VitalCheck(private val context: android.content.Context) {
    private var sensorManager: SensorManager? = null
    private var heartRateSensor: Sensor? = null
    private var heartRate: Float = 0f
    private var bodyTemperature: Float = 0f
    private var irregularHeartRhythmDetected = false
    var InDanger = false

    private val heartRateListener = object : SensorEventListener {
        override fun onSensorChanged(event: SensorEvent) {
            if (event.sensor.type == Sensor.TYPE_HEART_RATE) {
                heartRate = event.values[0]
                checkHeartRate()
            }
        }

        override fun onAccuracyChanged(sensor: Sensor, accuracy: Int) {}
    }

    private fun checkHeartRate() {
        if (heartRate < 40 || heartRate > 120) {
            irregularHeartRhythmDetected = true
            InDanger = true
        } else {
            irregularHeartRhythmDetected = false
        }
    }

    private fun checkBodyTemperature() {
        val healthServicesClient = HealthServices.getClient(context)
        healthServicesClient.getHealthData(
            HealthServicesClient.DataRequest.Builder()
                .setDataType(HealthServicesClient.DataType.BODY_TEMPERATURE)
                .build()
        )
            .addOnSuccessListener { data ->
                bodyTemperature = data.value
                if (bodyTemperature < 35 || bodyTemperature > 40) {
                    InDanger = true
                }
            }
            .addOnFailureListener { e ->
                Log.e("VitalCheck", "Failed to get body temperature", e)
            }
    }

    fun startCheckingVitals() {
        sensorManager = context.getSystemService(android.content.Context.SENSOR_SERVICE) as SensorManager
        heartRateSensor = sensorManager?.getDefaultSensor(Sensor.TYPE_HEART_RATE)
        sensorManager?.registerListener(heartRateListener, heartRateSensor, SensorManager.SENSOR_DELAY_NORMAL)

        CoroutineScope(Dispatchers.IO).launch {
            while (true) {
                checkBodyTemperature()
                delay(10000) // that's 10 seconds fyi, to preserve battery by not constantly spamming the check
            }
        }
    }

    fun stopCheckingVitals() {
        sensorManager?.unregisterListener(heartRateListener)
    }
}
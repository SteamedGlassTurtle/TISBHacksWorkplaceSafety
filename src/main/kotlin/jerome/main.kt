package main.kotlin.jerome

import main.kotlin.jerome.VitalCheck
import main.kotlin.jerome.Action

class main(private val context: android.content.Context) {
    private val vitalCheck = VitalCheck(context)
    private val action = Action(context)

    fun cat() {
        if (vitalCheck.InDanger) {
            action.execute()
        }
    }
}
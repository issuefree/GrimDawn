#Requires AutoHotkey v2.0
#SingleInstance
#Include timlib.ahk

mortar := spell("s", 15000, 200)
thermite := spell("d", 5000, 200)
slam := spell("f", 3000)
warcry := spell("e", 7500)

~LButton::{
	if WinActive("Grim Dawn") {
		queueL := []
		clockL := 0
		queueSpell(&queueL, slam, 0)
		queueSpell(&queueL, warcry, 250)
		queueSpell(&queueL, thermite, 500)
		queueSpell(&queueL, mortar, 1000)

		while GetKeyState("LButton", "p") {	
			processQueue(&queueL, &clockL)
		}
	}
}
#Requires AutoHotkey v2.0
#SingleInstance
#Include timlib.ahk

burst 			:= spell("s", 10000, 200)
warCry		 	:= spell("d", 20000, 200)
madness		 	:= spell("r", 3000, 200)
slamL 			:= spell("9", 3500, 200)
slamR 			:= spell("0", 3500, 200)

~*LButton::{
	if WinActive("Grim Dawn") {
		queueL := []
		clockL := 0
		queueSpell(&queueL, slamL, 0)
		queueSpell(&queueL, slamR, 0)
		queueSpell(&queueL, warCry, 250)
		queueSpell(&queueL, burst, 500)
		queueSpell(&queueL, madness, 500)

		while GetKeyState("LButton", "p") {	
			processQueue(&queueL, &clockL)
		}
	}
}
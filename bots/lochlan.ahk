#Requires AutoHotkey v2.0
#SingleInstance
#Include timlib.ahk

stormTotem 		:= spell("d", 4300, 250)
wendigoTotem 	:= spell("q", 5000, 200)
warCry 			:= spell("w", 5000, 200)
primalStrike 	:= spell("e", 1000, 200)  ; spam
oleronsMight 	:= spell("r", 3500, 200)

~*LButton::{
	if WinActive("Grim Dawn") {
		queueL := []
		clockL := 0
		queueSpell(&queueL, primalStrike, 0)
		queueSpell(&queueL, oleronsMight, 0)
		queueSpell(&queueL, warCry, 500)
		queueSpell(&queueL, stormTotem, 500)
		queueSpell(&queueL, wendigoTotem, 500)

		while GetKeyState("LButton", "p") {	
			processQueue(&queueL, &clockL)
		}
	}
}
return

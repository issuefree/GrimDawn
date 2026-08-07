#Requires AutoHotkey v2.0
#SingleInstance
#Include timlib.ahk

flashBang 	:= spell("f", 3000)
cocktail 	:= spell("d", 2000)
breath 		:= spell("e", 3000, 1500)
spread 		:= spell("r", 3000)

~*RButton::{
	if WinActive("Grim Dawn") {
		queueR := []
		clockR := 1
		queueSpell(&queueR, flashBang, 250)
		queueSpell(&queueR, cocktail, 500)
		queueSpell(&queueR, breath, 500)
		queueSpell(&queueR, spread, 500)

		while GetKeyState("RButton", "p") {	
			processQueue(&queueR, &clockR)
		}
	}
}
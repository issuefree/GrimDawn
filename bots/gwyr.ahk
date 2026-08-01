#Requires AutoHotkey v2.0
#SingleInstance
#Include timlib.ahk

flashBang 	:= spell("a", 3000) ; really 1 second but this isn't worth spamming
iceTrap 	:= spell("d", 3700)
fireTrap 	:= spell("f", 3700)
seal 		:= spell("s", 5000)
mortar 		:= spell("q", 15000)
thermite 	:= spell("w", 5000)
gaze 		:= spell("9", 6000)
breath 		:= spell("0", 3000)

~*LButton::{
	if WinActive("Grim Dawn") {
		queueL := []
		clockL := 0
		queueSpell(&queueL, flashBang, 250)
		queueSpell(&queueL, gaze, 500)
		; queueSpell(&queueL, breath, 500)

		while GetKeyState("LButton", "p") {	
			if GetKeyState("Shift", "p") {
				processQueue(&queueL, &clockL)
			}
		}
	}
}

~*RButton::{
	if WinActive("Grim Dawn") {
		queueR := []
		clockR := 0
		queueSpell(&queueR, iceTrap, 0)
		queueSpell(&queueR, fireTrap, 0)
		queueSpell(&queueR, seal, 0)
		queueSpell(&queueR, thermite, 250)
		queueSpell(&queueR, mortar, 1000)

		while GetKeyState("RButton", "p") {	
			processQueue(&queueR, &clockR)
		}
	}
}

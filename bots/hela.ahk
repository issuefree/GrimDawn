#Requires AutoHotkey v2.0
#SingleInstance
#Include timlib.ahk

reap 			:= spell("d", 2800)
siphon		 	:= spell("s", 4100, 250)

~*RButton::{
	if WinActive("Grim Dawn") {
		queueR := []
		clockR := 0
		queueSpell(&queueR, reap, 0)
		queueSpell(&queueR, siphon, 250)

		while GetKeyState("RButton", "p") {	
			processQueue(&queueR, &clockR)
		}
	}
}
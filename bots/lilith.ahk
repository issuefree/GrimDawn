#Requires AutoHotkey v2.0
#SingleInstance
#Include timlib.ahk

doombolt 	:= spell("s", 3900)
reap 		:= spell("s", 3000)
call 		:= spell("d", 20900)
blood 		:= spell("f", 10400)

~*LButton::{
	if WinActive("Grim Dawn") {
		queueL := []
		clockL := 0
		queueSpell(&queueL, reap, 0)
		queueSpell(&queueL, blood, 250)
		queueSpell(&queueL, call, 250)

		while GetKeyState("LButton", "p") {	
			if GetKeyState("Shift", "p") {
				processQueue(&queueL, &clockL)
			}
		}
	}
}
#Requires AutoHotkey v2.0
#SingleInstance
#Include timlib.ahk

rally	 	:= spell("a", 4000)
rip         := spell("d", 1000, 250)
frailty		:= spell("s", 2500, 250)
slam        := spell("f", 1000, 150)
leap        := spell("w", 1500, 250)
blood       := spell("q", 3000, 150)
greenpot    := spell("x", 6000, 150)
cry         := spell("e", 3000, 250)

~*LButton::{
	if WinActive("Grim Dawn") {
		queueL := []
		clockL := 0
		queueSpell(&queueL, frailty, 250)
		queueSpell(&queueL, cry, 250)
		queueSpell(&queueL, rip, 500)
		queueSpell(&queueL, leap, 500)
		queueSpell(&queueL, slam, 500)
		queueSpell(&queueL, rally, 750)
		queueSpell(&queueL, blood, 750)
		queueSpell(&queueL, greenpot, 1500)

		while GetKeyState("LButton", "p") {	
			; if GetKeyState("Shift", "p") {
				processQueue(&queueL, &clockL)
			; }
		}
	}
}

~*RButton::{
	if WinActive("Grim Dawn") {
		queueR := []
		clockR := 0
		; queueSpell(&queueR, rip, 500)
		; queueSpell(&queueR, leap, 100)

		while GetKeyState("RButton", "p") {	
			processQueue(&queueR, &clockR)
			SendInput "d"
		}
	}
}

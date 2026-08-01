#Requires AutoHotkey v2.0
#SingleInstance
#Include timlib.ahk

rally	 	:= spell("a", 8000)
burst	 	:= spell("s", 10000, 500)
slam        := spell("q", 1000, 150)
strike      := spell("w", 1750, 250)
leap        := spell("d", 1500, 250)
blades      := spell("e ", 1500, 250)
ring        := spell("f ", 1500, 150)
greenpot    := spell("x", 6000, 150)

~*LButton::{
	if WinActive("Grim Dawn") {
		queueL := []
		clockL := 0
		queueSpell(&queueL, rally, 250)
		queueSpell(&queueL, burst, 250)
		queueSpell(&queueL, strike, 500)
		queueSpell(&queueL, slam, 500)
		queueSpell(&queueL, blades, 500)
		queueSpell(&queueL, ring, 500)
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

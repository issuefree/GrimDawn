#Requires AutoHotkey v2.0
#SingleInstance
#Include timlib.ahk

rally	 	:= spell("a", 8000)			; buff and minor heal
burst	 	:= spell("s", 10000, 500)   ; buff and minor heal
sacred      := spell("q", 1500, 150)    ; strong single target and bebuff
shadow      := spell("w", 1750, 250)    ; dash single target (fast)
leap        := spell("d", 1500, 250)    ; dash multi target
ring        := spell("f ", 1500, 150)   ; pbaoe
cry         := spell("r", 4500, 250)    ; pbaoe debuff
greenpot    := spell("x", 6000, 150)    ; restore energy

~*LButton::{
	if WinActive("Grim Dawn") {
		queueL := []
		clockL := 0
		queueSpell(&queueL, rally, 250)
		queueSpell(&queueL, burst, 250)
		queueSpell(&queueL, shadow, 500)
		queueSpell(&queueL, cry, 500)
		queueSpell(&queueL, sacred, 500)
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
			SendInput leap.key
		}
	}
}

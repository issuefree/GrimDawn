#Requires AutoHotkey v2.0
#SingleInstance
#Include timlib.ahk

aegis 		:= spell("d", 500)  ; want this to spam a bit
stomp	 	:= spell("9", 5000, 200)
overguard	:= spell("w", 5000, 200)  ; gonna hit these more often since they have long cooldowns
ascension	:= spell("e", 5000, 200)
bladeWard	:= spell("r", 3000, 200)
warCry		:= spell("f", 7500, 200)
; forcewave	:= spell("q", 2800, 250)
; olliesMight	:= spell("9", 3500, 200)
dreegsGaze	:= spell("9", 2500, 175)
shieldSlam	:= spell("0", 3000, 200)
judgement	:= spell("r", 4800, 200)

~*LButton::{
	if WinActive("Grim Dawn") {
		queueL := []
		clockL := 0
		queueSpell(&queueL, shieldSlam, 0)
		queueSpell(&queueL, dreegsGaze, 0)
		queueSpell(&queueL, judgement, 250)
		queueSpell(&queueL, warCry, 500)
		queueSpell(&queueL, overguard, 500)
		queueSpell(&queueL, ascension, 500)

		while GetKeyState("LButton", "p") {	
			processQueue(&queueL, &clockL)
			SendInput aegis.key
		}
	}
}
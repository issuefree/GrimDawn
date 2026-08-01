#Requires AutoHotkey v2.0
#SingleInstance
#Include timlib.ahk

swarm 			:= spell("s", 3600)
bloodthirster 	:= spell("d", 20000, 200)
silverSpread 	:= spell("f", 3000, 500) ; has a "shotgun" effect so let's only use it at close range
wendigo 		:= spell("0", 10000, 300)

dreegBlood		:= spell("q", 15000)

frailty 		:= spell("w", 9600)
graspingVines 	:= spell("e", 4500)
pox 			:= spell("r", 6000)
stormTotem 		:= spell("9", 5000)

~*LButton::{
	if WinActive("Grim Dawn") {
		queueL := []
		clockL := 0
		queueSpell(&queueL, swarm, 0)
		queueSpell(&queueL, silverSpread, 250)
		queueSpell(&queueL, wendigo, 250)
		queueSpell(&queueL, bloodthirster, 500)
		queueSpell(&queueL, dreegBlood, 500)
		
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
		queueSpell(&queueR, frailty, 0)
		queueSpell(&queueR, graspingVines, 0)
		queueSpell(&queueR, pox, 0)
		queueSpell(&queueR, stormTotem, 250)
		queueSpell(&queueR, dreegBlood, 500)

		while GetKeyState("RButton", "p") {	
			processQueue(&queueR, &clockR)
		}
	}
}
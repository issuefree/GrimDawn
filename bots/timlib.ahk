#UseHook

SetKeyDelay 50

log(s) {
	FileAppend(s "`n", "grimdawn.log")
}

logQueue(queue) {
	log("queue:")
	for spell in queue {
		log(spell.key)
	}
	log(".")
}

getDistance() {
	MouseGetPos(&x, &y)
	x := x - 1280
	y := y - 720
	return sqrt((x*x + y*y))
}

spell(key, cd, range:=0) {
	return {key:key, cd:cd, range:range}
}

queueSpell(&queue, spell, castTime) {
	spell.castTime := castTime
	queue.Push(spell)
}

getSoonestSpellIndex(spells) {
	minTime := 0
	minIndex := 0
	i := 0
	for (spell in spells) {
		i := 1
		if (minTime == 0 or spell.castTime < minTime) {
			minTime := spell.castTime
			minIndex := i
		}
	}
	return minIndex
}

tooSoon(spell, clock) {
	return clock < spell.castTime
}

tooFar(spell) {
	if (spell.range > 0) {
		return getDistance() > spell.range
	}
	return 0
}

getNextSpell(&queue, clock) {
	notReady := []
	ready := []
	while (queue.Length > 0) {
		spell := queue.RemoveAt(1)
		if (tooSoon(spell, clock) or tooFar(spell)) {
			notReady.Push(spell)
		} else {
			ready.Push(spell)
		}
	}
	for (spell in notReady) {
		queue.Push(spell)
	}
	if (ready.Length == 0) {
		return
	}
	soonestReadyIndex := getSoonestSpellIndex(ready)
	spell := ready.RemoveAt(soonestReadyIndex)
	for (reject in ready) {
		queue.Push(reject)
	}
	queueSpell(&queue, spell, clock + spell.cd + 250)
	return spell
}

processQueue(&queue, &clock) {
	spell := getNextSpell(&queue, clock)
	if (spell) {
		key := spell.key

		SendInput "{" key " down}"
		Sleep 100
		SendInput "{" key " up}"
	}
	Sleep 250
	clock += 250
}

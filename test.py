duration = 4.0
recharge = 10.0
fightLength = 60.0

print duration/(duration+recharge)*fightLength

print duration/(duration+recharge)*(fightLength-duration) + duration

upTime = 0
while fightLength > 0:
	upTime += min(duration, fightLength)
	fightLength -= duration + recharge
print upTime
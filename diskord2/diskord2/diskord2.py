




from phone import Phone




p = Phone('', 3334, 5)


p.turn_on()

try:
	p.main_menu()
finally:
	p.turn_off()

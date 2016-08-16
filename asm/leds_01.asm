#light leds OUT0 = value from 0 to 255

	MOVI A,0
label1:
	OUT 0x00
	INC A
	JMP label1


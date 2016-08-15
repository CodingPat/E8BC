#light leds OUT0 = value from 0 to 255

MOVI A,0
OUT 0x00
INC A
JMP 0x0002


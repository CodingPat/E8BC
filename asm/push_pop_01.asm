// stack pointer = 0X00FF
MOVI SPH,0X00
MOVI SPL,0XFF


//save values of registers to stack
MOVI A,0X01
PUSH A

MOVI B,0X02
PUSH B

MOVI A,0X03
MOV H,A
PUSH H

MOVI A,0X04
MOV L,A
PUSH L

PUSH F

PUSH SPH

PUSH SPL


// reset values of registers
MOVI A,0X00
MOVI B,0X00
MOV H,A
MOV L,A


//get saved values back to registers

POP SPL
POP SPH
POP F
POP L
POP H
POP B
POP A

HLT





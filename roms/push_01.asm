# push_01.rom
# test push registers + cache registers 0-3 + memory adress

#stack at 00FF
MOVI SPL,1
MOVI SPH,1

#push regs

PUSH A
PUSH B
PUSH H
PUSH L
PUSH SPH
PUSH SPL
PUSH F
PUSH R0
PUSH R1
PUSH R2
PUSH R3
PUSH M,0x0004

#END
HLT


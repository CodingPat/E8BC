# push_01.rom
# test push registers + cache registers 0-3 + memory adress

#stack at 00FF
MOVI SPL,FF
MOVI SPH,01

#push regs

PUSH A
PUSH B
PUSH H
PUSH L
PUSH SPH
PUSH SPL
PUSH F
PUSH REG0
PUSH REG1
PUSH REG2
PUSH REG3
PUSH M,0004

#END
HLT


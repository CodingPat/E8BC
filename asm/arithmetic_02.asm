#opérations arithmétiques sur 8 bits
#opérande 1 = IN 00
#opérande 2 = IN 01
# ADD = OUT 00
# SUB = OUT 01
# MUL = OUT 02
# DIV = OUT 03


  MOVI A,0

LOOP:
  IN 01
  MOV B,A
  IN 00
  ADD B
  OUT 00
  
  IN 01
  MOV B,A
  IN 00
  SUB B
  OUT 01



  IN 01
  MOV B,A
  IN 00
  MUL B
  OUT 02

  IN 01
  MOV B,A
  IN 00
  DIV B
  OUT 03
  
  JMP LOOP
  HLT
  
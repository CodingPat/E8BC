#opérations arithmétiques sur 8 bits
#opérande 1 = port 00
#opérande 2 = port 01
#résultat = port 02

  MOVI A,0

LOOP:
  IN 00
  MOV B,A
  IN 01
  ADD B
  OUT 02
  JMP LOOP
  HLT
  
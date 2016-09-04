# opérations arithmétiques sur 8 bits
# opérande 1 = IN 00
# opérande 2 = IN 01
# operation = IN02 (0=no operation - 1=ADD - 2=SUB - 3=MUL - 4=DIV)
# RESULT= OUT 00

  MOVI A,0

LOOP:
  #store operands
  IN 00
  MOV 0x0000,A
  IN 01
  MOV 0x0001,A
  
  #store operator
  IN 02
  MOV 0x0002,A
  
  #test operator=+
  MOV A,0x0002
  MOVI B,1
  SUB B
  JZ ADD
  
  #test operator=-
  MOV A,0x0002  
  MOVI B,2
  SUB B
  JZ SUB

  #test operator=*
  MOV A,0x0002  
  MOVI B,4
  SUB B
  JZ MUL

  #test operator=/
  MOV A,0x0002
  MOVI B,8
  SUB B
  JZ DIV
  
  #no operation reset
  MOVI A,0x00
  JMP DISPLAY  
  
  
ADD:
  MOV A,0x0000
  MOV B,0x0001
  ADD B
  JMP DISPLAY

SUB:
  MOV A,0x0000
  MOV B,0x0001
  SUB B
  JMP DISPLAY

MUL:
  MOV A,0x0000
  MOV B,0x0001
  MUL B
  JMP DISPLAY

DIV:
  MOV A,0x0000
  MOV B,0x0001
  DIV B
  JMP DISPLAY


DISPLAY:
  OUT 00
  
  
  JMP LOOP
  HLT
  
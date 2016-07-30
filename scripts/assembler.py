import sys
import re

class Parser():
  """parse a file and return elements for each line"""
  
  def __init__(self,opcodes):
    self.parsed_line={}
    self.opcodes=opcodes
    
  def parse_line(self,line):
    """read line """
    line=line.strip()
    instruction_type=self.instruction_type(line)
          
    if instruction_type=="comment":    
      self.parsed_line={'type':"comment",'line':line}
    
    elif instruction_type=="label":
      label=self.symbol()
      self.parsed_line={'type':"label",'label':label}
      
    elif instruction_type=="blank":
      self.parsed_line={'type':"blank",'line':line}
      
    elif instruction_type=="variable":
      variable=self.symbol()
      self.parsed_line={'type':'variable','variable':variable}
    
    elif instruction_type=="opcode":
      opcode=""
      source=""
      destination=""
      result=self.split_opcode(line)
      if result:
        self.parsed_line=result        
        self.parsed_line.update({'type':'opcode'})
        
      else:
        # bad format for instruction
        self.parsed_line={'type':None}

    
    else:
      self.parsed_line={'type':None}
     
      
  def split_opcode(self,line):
    """get opcode, source, destination"""
    opcode=""    
    operand1=""
    operand2=""
    line=line.upper()
    
    result=line.split(' ')
    
    if len(result)==1:
      opcode=result[0]
    if len(result)==2:
      opcode,other=result
      other=other.split(',')
      nr_operands=len(other)
      if nr_operands==1:
        operand1=other[0]
      elif nr_operands==2:
        operand1=other[0]
        operand2=other[1]
        
    return({'opcode':opcode,'operand1':operand1,'operand2':operand2})
    
  def instruction_type(self,line):
    """blank, label or instruction ?"""
    #delete comments
    line=line.split('#')
    
    line=line[0]
    
    matchobj=re.match(r'^[a-zA-Z]\w+:$',line)
    if matchobj:
      return "label"
      
    matchobj=re.match(r'^\s*$',line)
    if matchobj:
      return "blank"
    
    
    # search for opcode
    for opcode in self.opcodes:
      myreg=r'^'+opcode+'{1}'
      matchobj=re.match(myreg,line)
      if matchobj:
        return "opcode"
    
    # type unknown 
    return None
    

  def symbol(self):
    """return label or variable"""
    pass
    
  def get_destination(self):
    """return destination - call only if instruction type=opcode"""
    return(self.parsed_line['destination'])
    
    
  def get_source(self):
    """return source - call only if instruction type=opcode"""
    return(self.parsed_line['source'])

  def get_opcode(self):
    """return opcode - call only if instruction type=opcode"""
    return(self.parsed_line['opcode'])
    
    



class SymbolTable():
  pass
  



class Encoder():
  pass
    
  
class Controller():
  """controls the working of the parser"""
  def __init__(self,file_in,file_out,opcodes):
    self.file_in=open(file_in,'r')
    self.file_out=open(file_out,'w')
    self.parser=Parser(opcodes)
    
  def start(self):
    while True:
      line=self.file_in.readline()
      
      if line:
        self.parser.parse_line(line)
        result=self.parser.parsed_line
        print(result)
    
      else:
        break
        
     
  
if __name__=='__main__':
  # to do : replace set opcodes, by getting hash codes from table machine_code, 
  opcodes=set(['MOV','MOVI','ADD','ADC','OUT','IN','HLT','CLC','JMP','JZ','JLT','JGT','JNZ','INC','SUB','SBC','ORA','ANA','PUSH','POP','CALL','RET'])
  
  
  file_in=sys.argv[1]
  file_out=sys.argv[2]
  my_controller=Controller(file_in,file_out,opcodes)
  my_controller.start()
  
  
  

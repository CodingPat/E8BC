import sys
import re
import csv

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
  def __init__(self,mnemonics_file):
    self.mnemonics_regex=[]
    self.mnemonics_hex=[]
    self.instruction=""
    self.read_file(mnemonics_file)
    self.translated={'nr_bytes':0}
  
  def set_instruction(self,code_dict):
    self.instruction=code_dict['opcode']
    if code_dict['operand1']:
      self.instruction=self.instruction+' '+code_dict['operand1']
    if code_dict['operand2']:
      self.instruction=self.instruction+','+code_dict['operand2']
    self.instruction=self.instruction.strip()
    
  def encode(self,code_dict):
    self.set_instruction(code_dict)
    result=self.translate(self.instruction)
    print('hex : ',result)
    
     
  
  def read_file(self,mnemonics_file):
    with open(mnemonics_file) as csv_file:
      csv_reader=csv.reader(csv_file,delimiter=';')
      for row in csv_reader:
        self.mnemonics_regex.append(row[1])
        self.mnemonics_hex.append(row[2])
          
    
  def translate(self,mnemonic):
    #TO DO : some instructions are coded on multiple bytes. Return hex + number of bytes
    print('translate : ',mnemonic)    
    index=0
    opcode_hex=""
    for reg in self.mnemonics_regex:
      reg=reg.encode('unicode-escape').decode('utf-8')
      #print('regex :',reg)
      matchobj=re.match(reg,mnemonic)
      if matchobj:
        opcode_hex=self.mnemonics_hex[index]
        return({'hex':opcode_hex,'bytes':1})
      index=index+1
    return None   
    
    
  
class Controller():
  """controls the working of the parser"""
  def __init__(self,file_in,file_out,opcodes,mnemonics_file):
    self.file_in=open(file_in,'r')
    self.file_out=open(file_out,'w')
    self.parser=Parser(opcodes)
    self.encoder=Encoder(mnemonics_file)
    
  def start(self):
    while True:
      line=self.file_in.readline()
      
      if line:
        self.parser.parse_line(line)
        result=self.parser.parsed_line
        print(result)
        if result['type']=="opcode":        
          self.encoder.encode(result)
    
      else:
        break
        
       
  
if __name__=='__main__':
  #to do : replace opcodes set by sqlite3 file with instructions/opcode  
  opcodes=set(['MOV','MOVI','ADD','ADC','OUT','IN','HLT','CLC','JMP','JZ','JLT','JGT','JNZ','INC','SUB','SBC','ORA','ANA','PUSH','POP','CALL','RET'])
  
  
  file_in=sys.argv[1]
  file_out=sys.argv[2]
  mnemonics_file='mnemonics.csv'
  my_controller=Controller(file_in,file_out,opcodes,mnemonics_file)
  my_controller.start()
  
  
  

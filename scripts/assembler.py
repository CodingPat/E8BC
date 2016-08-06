import sys
import re
import csv



class Mnemonics():
  def __init__(self,mnemonics_file):
    self.regex=[]
    self.hex=[]
    self.read_file(mnemonics_file)
    
  def read_file(self,mnemonics_file):
    with open(mnemonics_file) as csv_file:
      csv_reader=csv.reader(csv_file,delimiter=';')
      for row in csv_reader:
        self.regex.append(row[1])
        self.hex.append(row[2])

    
    
    
    
class Parser():
  """parse a file and return elements for each line"""
  
  def __init__(self,mnemonics):
    self.parsed_line={}
    self.mnemonics=mnemonics
  
  
  def parse_for_blank(self,line):
    matchobj=re.match(r'^\s*$',line)
    if matchobj or line=="":
      self.parsed_line={'type':"blank",'line':line}
    else:
      return None
    
  
  def parse_for_symbol(self,line):
    #unfinished
    #test .variable=#<0000> or :<label>
    """matchobj=re.match(r'^[a-zA-Z]\w+:$',line)
    if matchobj:
      return "label"
    """
    pass

  def parse_for_opcode(self,line):
    index=0
    opcode_hex=""
    for reg in self.mnemonics.regex:
      #some black magic to decode string csv => raw string (needed for re.match)      
      #r'<expression>' means : raw string = do not interpretate escape character
      reg=reg.encode('unicode-escape').decode('utf-8')
      print('regex :',reg)
      matchobj=re.match(reg,line)
      if matchobj:
        return({'type':'opcode','regex':mnemonics.regex[index]})
      index=index+1
    return None   
    
  
    
  def parse_line(self,line):
    """read line """
    line=line.strip()
    self.parsed_line={}
    
    #delete comments
    line=line.split('#')
    line=line[0]

        
    result=self.parse_for_opcode(line)
    if result:
      self.parsed_line=result
    else:
      result=self.parse_for_blank(line)
      if result:
        self.parsed_line=result
      else:
        result=self.parse_for_symbol(line)
        if result:
          self.parsed_line=result
        else:
          self.parsed_line={'type':'unknown','line':line}
      
             
      
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
    
        
      
class SymbolTable():
  pass
  



class Encoder():
  def __init__(self):
    self.instruction=""
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
    
     
  def translate(self,mnemonic):
    #TO DO : some instructions are coded on multiple bytes. Return hex + number of bytes
    #print('translate : ',mnemonic)    
    pass
    
  
class Controller():
  """controls the working of the parser"""
  def __init__(self,file_in,file_out,mnemonics_file):
    self.file_in=open(file_in,'r')
    self.file_out=open(file_out,'w')
    self.mnemonics=Mnemonics(mnemonics_file)
    self.parser=Parser(self.mnemonics)
    self.encoder=Encoder()
    
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
  #to do : replace opcodes set by csv file with regex/hex  
    
  file_in=sys.argv[1]
  file_out=sys.argv[2]
  mnemonics_file='mnemonics.csv'
  my_controller=Controller(file_in,file_out,mnemonics_file)
  my_controller.start()
  
  
  

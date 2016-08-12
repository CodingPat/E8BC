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
      return {'type':"blank"}
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
      #transform reg in raw string (to be used as regex) 
      #print('regex :',reg)
      matchobj=re.match(reg,line)
      if matchobj:
        dic_instruction=self.split_opcode(line)
        dic_instruction.update({'type':'opcode','regex':self.mnemonics.regex[index]})
        return dic_instruction
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
  def __init__(self,mnemonics):
    self.mnemonics=mnemonics    
    self.translated=[]
    
  def operand_to_hex(self,operand):
    """convert operand to hex"""
    if re.match(r'^0x[0-9A-F]+$',operand):
      operand.replace("0x","")
      return operand
    elif re.match(r'^[0-9]+$'):
      operand=hex(operand).split('x')[1]
      return operand
    else:
      return None
    
    
  def extra_bytes(self,parse_dict):
    extra_bytes=[]
    if parse_dict['opcode'] in('CALL','IN','JGT','JLT','JMP','JNZ','JZ'):    
      result=str(operand_to_hex(parse_dict['operand1']))
      
        
    if result:
      extra_bytes.append(result[2,3])
      extra_bytes.append(result[0,1])

    return extra_bytes      
      
  def encode(self,parse_dict):
    self.translated=[]
    index=self.mnemonics.regex.index(parse_dict['regex'])
    if index:
      self.translated.append(self.mnemonics.hex[index])

      #multibytes instructions
      if parse_dict['opcode'] in('CALL','IN','JGT','JLT','JMP','JNZ','JZ'):
        result=self.extra_bytes(parse_dict)
        if result:
          self.translated.append(result)
        else:
          print('ERROR ENCODING MULTIBYTE INSTRUCTION')
      
      print(parse_dict['opcode'],parse_dict['operand1'],parse_dict['operand2'],'\tHex : ',self.translated)
      
    else:
      print("ERROR NO HEX FOUND")
        
     
     
  
class Controller():
  """controls the working of the parser"""
  def __init__(self,file_in,file_out,mnemonics_file):
    self.file_in=open(file_in,'r')
    self.file_out=open(file_out,'w')
    self.mnemonics=Mnemonics(mnemonics_file)
    self.parser=Parser(self.mnemonics)
    self.encoder=Encoder(self.mnemonics)
    
  def start(self):
    while True:
      line=self.file_in.readline()
      
      if line:
        self.parser.parse_line(line)
        result=self.parser.parsed_line
        if result['type']=="unknown":
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
  
  
  



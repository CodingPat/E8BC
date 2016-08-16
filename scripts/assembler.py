import sys
import re
import csv
import os

class SymbolTable():
  def __init__(self):
    self.symbols={}
    self.next_free_address=0
    
  def addEntry(self,symbol):
    address=str(hex(self.next_free_address)).upper()
    address.replace('0X','').zfill(4)
    address='0X'+address    
    self.symbols['symbol']=address
    self.next_free_address=self.next_free_address+1
  
  def contains(self,symbol):
    if self.symbols['symbol']:
      return True
    else:
      return False
    
  def getAddress(self,symbol):
    if self.contains(symbol):
      return self.symbols['symbol']
    else:
      return None
    

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
  
  def __init__(self,mnemonics,symbols):
    self.parsed_line={}
    self.mnemonics=mnemonics
    self.symbols=symbols
  
  
  def parse_for_blank(self,line):
    matchobj=re.match(r'^\s*$',line)
    if matchobj or line=="":
      return {'type':"blank"}
    else:
      return None
    
  
  def parse_for_label(self,line):
    matchobj=re.match(r'^\w+:$',line)
    line.replace(":","")
    if matchobj:
      if not self.symbols.gets(line):
        self.symbols.add_entry(line)
       
      return {'type':"label"}
    
    

  def parse_for_opcode(self,line):
    index=0
    opcode_hex=""
    for reg in self.mnemonics.regex:
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
        result=self.parse_for_label(line)
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
    
        
      
class Encoder():
  def __init__(self,mnemonics):
    self.mnemonics=mnemonics    
    self.translated=[]
    
  def operand_to_hex(self,operand):
    """convert operand to hex"""
    if re.match(r'^0X[0-9A-F]+$',operand):
      return operand
    elif re.match(r'^[0-9]+$',operand):
      operand=hex(int(operand)).split('x')[1]
      if len(operand)<2:
        operand=operand.zfill(2)
      elif len(operand)<4:
        operand=operand.zfill(4)
      operand='0X'+operand
      return operand
    else:
      return None
    
    
  def extra_bytes(self,parse_dict):
    extra_bytes=[]
    result=""
    
    if parse_dict['opcode'] in('CALL','IN','JGT','JLT','JMP','JNZ','JZ'):    
      result=str(self.operand_to_hex(parse_dict['operand1']))
      if result:
        result=result.split('0X')[1]
        extra_bytes.append(result[2:4])
        extra_bytes.append(result[0:2])
    
    if parse_dict['opcode'] in('OUT'): 
      result=str(self.operand_to_hex(parse_dict['operand1']))
      if result:
        result=result.split('0X')[1]
        extra_bytes.append(result)
          
         
    if parse_dict['opcode'] in('MOVI'):    
      result=str(self.operand_to_hex(parse_dict['operand2']))
      if result:
        result=result.split('0X')[1]
        extra_bytes.append(result)
       
    if parse_dict['opcode']=='PUSH' and parse_dict['operand1'][0]=='R':    
      operand=parse_dict['operand1'].split('R')[1] 
      result=str(self.operand_to_hex(operand))
      if result:
        result=result.split('0X')[1]
        extra_bytes.append(result)
      
    if parse_dict['opcode']=='PUSH' and parse_dict['operand1']=='M':    
      operand=parse_dict['operand2']
          
      result=str(self.operand_to_hex(operand))
      if result:      
        result=result.split('0X')[1]
        extra_bytes.append(result[2:4])
        extra_bytes.append(result[0:2])
        #use temporary register reg0
        extra_bytes.insert(0,'00')
    
    if not result:
      print('ERROR - OPERAND VALUE NOT VALID')

    return extra_bytes      
      
  def encode(self,parse_dict):
    self.translated=[]
    index=self.mnemonics.regex.index(parse_dict['regex'])
    multibyte=False
    if index:
      self.translated.append(self.mnemonics.hex[index])

      #multibytes instructions
      if parse_dict['opcode'] in('CALL','IN','JGT','JLT','JMP','JNZ','JZ','MOVI'):
        multibyte=True        
      elif parse_dict['opcode']=="PUSH" and (parse_dict['operand1'][0]=='R' or parse_dict['operand1']=='M'):
        multibyte=True
      elif parse_dict['opcode']=="OUT":
        multibyte=True
      
      if multibyte :
        result=self.extra_bytes(parse_dict)
        if result:
          self.translated=self.translated+result
        else:
          print('ERROR ENCODING MULTIBYTE INSTRUCTION')

    else:
      print("ERROR NO HEX FOUND")
        
     
class Writer():
  def __init__(self,file_rom,file_txt):
    self.file_rom=file_rom
    self.file_txt=file_txt  
    self.bytes_written=0
    self.write_header()
  
  def write_header(self):
    self.file_rom.write("v2.0 raw\n")
    
  def write_to_file(self,hex_array,line_code):
    
    #write to txt
    rom_address=str(hex(self.bytes_written)).replace('0x',"").zfill(4)
    rom_address="0X"+rom_address    
    line=str(rom_address).ljust(10)+" ".join(hex_array).ljust(15)+line_code.strip()
    self.file_txt.write(line+'\n')
    
    
    #write to rom    
    nr_bytes_to_write=len(hex_array)
    while(nr_bytes_to_write):    
      nr_bytes_to_write=nr_bytes_to_write-1    
      byte=hex_array.pop(0)
      self.file_rom.write(byte+" ")
      self.bytes_written=self.bytes_written+1
      if self.bytes_written%8==0:
        self.file_rom.write('\n')
        
   
     
  
class Controller():
  """controls the working of the parser"""
  def __init__(self,file_in,mnemonics_file):
    self.file_in=open(file_in,'r')
    file_name=os.path.basename(file_in)
    file_path=file_in.replace(file_name,"")
    
    file_name=file_name.split('.asm')[0]
        
    file_rom=file_name+'.rom'
    file_rom=os.path.join(file_path,file_rom)    
    file_txt=file_name+'.txt'
    file_txt=os.path.join(file_path,file_txt)    
    
    print(file_rom,file_txt)   
    self.file_rom=open(file_rom,'w')
    self.file_txt=open(file_txt,'w')    
    self.mnemonics=Mnemonics(mnemonics_file)
    self.parser=Parser(self.mnemonics)
    self.encoder=Encoder(self.mnemonics)
    self.writer=Writer(self.file_rom,self.file_txt) 
    
  #TO DO : 2 passes. 
  #First pass=file.1st (txt) + create symbol table
  #Second pass = file.txt + file.rom : replace symbols by addresses
  
  def start(self):
    while True:
      line=self.file_in.readline()
      
      if line:
        line=line.upper()
        self.parser.parse_line(line)
        result=self.parser.parsed_line
        #print(result)
        if result['type']=="unknown":
          print("ERROR :",result)
        if result['type']=="opcode":
          self.encoder.encode(result)
          
          #print(" ".join(self.encoder.translated)+"\t\t"+self.parser.parsed_line['opcode'])
          self.writer.write_to_file(self.encoder.translated,line)
                     
      else:
        break
      
    self.file_in.close()
    self.file_rom.close()
    self.file_txt.close()
        
       
  
if __name__=='__main__':
  #to do : replace opcodes set by csv file with regex/hex  
    
  file_in=sys.argv[1]
  mnemonics_file='mnemonics.csv'
  my_controller=Controller(file_in,mnemonics_file)
  my_controller.start()
  
  
  



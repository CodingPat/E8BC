import sys
import re
import csv
import os
import fileinput

class SymbolTable():
  def __init__(self):
    self.table={}
        
  def addEntry(self,symbol,address):
    self.table[symbol]=address
    
  
  def contains(self,symbol):
    if symbol in self.table:
      return True
    else:
      return False
    
  def getAddress(self,symbol):
    if symbol in self.table:
      return self.table[symbol]
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
  
  def __init__(self,mnemonics,symbol_table):
    self.parsed_line={}
    self.mnemonics=mnemonics
    self.symbol_table=symbol_table
  
  
  def parse_for_blank(self,line):
    matchobj=re.match(r'^\s*$',line)
    if matchobj or line=="":
      return {'type':"blank"}
    else:
      return None
    
  
  def parse_for_label(self,line):
    line.strip()
    matchobj=re.match(r'^\w+:$',line)
    line.replace(":","")
    if matchobj:
      return {'type':"label",'label':line}
    
    

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

        
  def parse_for_symbol():
  #check for symbol
    for operand in ['operand1','operand2']:
    
      if self.parsed_line[operand]:
        if re.match(r'^[a-zA-Z]\w+$',self.parsed_line[operand]):
          if not self.symbols.contains(self.parsed_line[operand]):
            self.symbols.addEntry(self.parsed_line[operand])
        
                  
      
class Encoder():
  encoded_bytes=0 #class variable= total number of bytes encoded so far
  
  def __init__(self,mnemonics):
    self.mnemonics=mnemonics    
    self.translated=[]
    self.nr_bytes=0 #nr bytes is different of len(self.translated) because of symbols
    
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
    
    if parse_dict['opcode'] in('CALL','JGT','JLT','JMP','JNZ','JZ'):
      if re.match(r'^[a-zA-Z]\w+$',parse_dict['operand1']):
      #label symbol
        #write 2 values to keep the number of bytes written correct
        result='?'+parse_dict['operand1']+'?'        
        extra_bytes.append(result)
        
      else:      
      #value
        result=str(self.operand_to_hex(parse_dict['operand1']))
        if result:
          result=result.split('0X')[1]
          extra_bytes.append(result[2:4])
          extra_bytes.append(result[0:2])

      self.nr_bytes=self.nr_bytes+2
      
    if parse_dict['opcode'] in('IN','OUT'): 
      if re.match(r'^[a-zA-Z]\w+$',parse_dict['operand1']):
      #variable symbol (IN/OUT use 8bits address)
        result="?"+parse_dict['operand1']+"?"
        extra_bytes.append(result)
      else:
      #value
        result=str(self.operand_to_hex(parse_dict['operand1']))
        if result:
          result=result.split('0X')[1]
          extra_bytes.append(result)
      
      self.nr_bytes=self.nr_bytes+1      
         
    if parse_dict['opcode'] in('MOVI'):    
      if re.match(r'^[a-zA-Z]\w+$',parse_dict['operand1']):
      #variable symbol
        result="?"+parse_dict['operand2']+"?"
        extra_bytes.append(result) 
      else:
      #value       
        result=str(self.operand_to_hex(parse_dict['operand2']))
        if result:
          result=result.split('0X')[1]
          extra_bytes.append(result)
       
      self.nr_bytes=self.nr_bytes+1
       
    if parse_dict['opcode']=='PUSH' and parse_dict['operand1'][0]=='R':    
      operand=parse_dict['operand1'].split('R')[1] 
      result=str(self.operand_to_hex(operand))
      if result:
        result=result.split('0X')[1]
        extra_bytes.append(result)
        self.nr_bytes=self.nr_bytes+1
      
    if parse_dict['opcode']=='PUSH' and parse_dict['operand1']=='M':    
      operand=parse_dict['operand2']
          
      result=str(self.operand_to_hex(operand))
      if result:      
        result=result.split('0X')[1]
        extra_bytes.append(result[2:4])
        extra_bytes.append(result[0:2])
        #use temporary register reg0
        extra_bytes.insert(0,'00')
        self.nr_bytes=self.nr_bytes+3
    
    return extra_bytes      
      
  def encode(self,parse_dict):
    self.translated=[]
    self.nr_bytes=0
    index=self.mnemonics.regex.index(parse_dict['regex'])
    multibyte=False
    if index:
      self.translated.append(self.mnemonics.hex[index])
      self.nr_bytes=self.nr_bytes+1

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
    
    Encoder.encoded_bytes=Encoder.encoded_bytes+self.nr_bytes
      
     
       
     
class Writer():
  def __init__(self,file_txt):
    self.file_txt=file_txt  
    
        
  def write_instruction(self,hex_array,nr_bytes,line_code):
    
    #write to txt
    rom_address=str(hex(Encoder.encoded_bytes-nr_bytes)).replace('0x',"").zfill(4)
    rom_address="0X"+rom_address    
    line=str(rom_address).ljust(10)+" ".join(hex_array).ljust(30)+line_code.strip()
    self.file_txt.write(line+'\n')
    
    
  def write_label(self,result):
    self.file_txt.write(result['label']+'\n')
            
   
class MemoryManager():
  
  def __init__(self,first_free_address="0x0000",last_free_address="0xFFFF"):
    self.next_free_address=first_free_address
    self.last_free_address=last_free_address
  
  def allocate_memory(self,nr_bytes):
    #to do : check upper limit self.last_free_address
    result=self.next_free_address
    self.next_free_address=self.next_free_address+nr_bytes
    return result
    
    
  def set_next_free_address(self,address):
    self.next_free_address=address
    

  
class Controller():
  """controls the working of the parser"""
  def __init__(self,file_in,mnemonics_file):
    self.file_in=open(file_in,'r')
    file_out=file_in.replace(".asm",".txt")    
    self.file_out=open(file_out,'r+')
      
    self.mnemonics=Mnemonics(mnemonics_file)
    self.symbol_table=SymbolTable()
    self.parser=Parser(self.mnemonics,self.symbol_table)
    self.encoder=Encoder(self.mnemonics)
    self.writer=Writer(self.file_out)
    
    self.memory_manager=MemoryManager() 
  


   
  def start(self):
  
  #Two passes are needed to resolve symbols  
  #it's not possible to resolve all label symbols at first pass
  #you can read an instruction JMP <label> before the label symbol has been resolved
  #At first pass :
  # -the labels are added to the symbol table (to avoid a complete reparsing at second pass to get the address)     
  # -symbols are prefixed and suffixed by ?, like this : ?symbol?, to help the second pass recognize symbols to solve 
  

    self.first_pass()
    self.second_pass()
    
  def first_pass(self):
    
    print("\nStarting first pass")
    print("=============================================")
    while True:
      line=self.file_in.readline()
    
      if line:
        line=line.upper()
        self.parser.parse_line(line)
        result=self.parser.parsed_line
        if result['type']=="unknown":
          print("ERROR :",result)
          break
        if result['type']=="opcode":
          self.encoder.encode(result)
          self.writer.write_instruction(self.encoder.translated,self.encoder.nr_bytes,line)
        if result['type']=="label":
          self.writer.write_label(result)
          result=result['label'].replace(':','')
          address='0x'+str(hex(Encoder.encoded_bytes)).replace('0x','').zfill(4)
          self.symbol_table.addEntry(result,address)
                   
      else:
        break
          
    print("Encoded bytes:",Encoder.encoded_bytes)
    print('symbol table for labels:',self.symbol_table.table)
  
    
            
  def second_pass(self):
    print("\nStarting second pass to resolve all symbols")
    print("=============================================")
    #second pass = replace symbols by addresses in file file.txt 
        
    self.file_out.seek(0)    
    record_nr=-1
    
    line=self.file_out.readline().strip()    
    while line:
      record_nr=record_nr+1
      result=re.search(r'\?\w+\?',line)
      if result:
        symbol=result.group()
        print('line',record_nr,'symbol:',symbol)
          
      line=self.file_out.readline().strip()
          
      
  
    
    
    #write to rom (logisim format 8 bytes per line)
    #def write_header(self):
    #self.file_rom.write("v2.0 raw\n")
     
    #nr_bytes_to_write=len(hex_array)
    #while(nr_bytes_to_write):    
    #  nr_bytes_to_write=nr_bytes_to_write-1    
    #  byte=hex_array.pop(0)
    #  self.file_rom.write(byte+" ")
    #  self.bytes_written=self.bytes_written+1
    #  if self.bytes_written%8==0:
    #    self.file_rom.write('\n')
    
    
    
      
    self.file_in.close()
    self.file_out.close()
        
       
  
if __name__=='__main__':
  #to do : replace opcodes set by csv file with regex/hex  
    
  file_in=sys.argv[1]
  print(file_in)
  mnemonics_file='mnemonics.csv'
  my_controller=Controller(file_in,mnemonics_file)
  my_controller.start()
  
  
  



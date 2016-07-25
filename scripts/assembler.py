import sys
import re

class Parser():
  """parse a file and return elements for each line"""
  
  def __init__(self):
    pass

  def parse_line(self,line):
    """read line """
    line=line.strip()
    if line:
      instruction_type=self.instruction_type(line)
    else:
      return({'type':"blank",'line':line})
        
    if instruction_type=="comment":    
      return({'type':"comment",'line':line})
    elif instruction_type=="label":
      label=symbol()
      return({'type':"label",'label':label})
    elif instruction_type=="blank":
      return({'type':"blank",'line':line})
    elif instruction_type=="variable":
      return({'type':'variable'})
    else:
      #must be opcode
      opcode=""
      source=""
      destination=""
      result=self.split_opcode(line)
      if result:
        result.update({'type':'opcode'})
        return(result)
      else:
        return({'type':None})
      
  def split_opcode(self,line):
    """get opcode, source, destination"""
    source=""
    destination=""
    line=line.upper()
    print(line)
    result=line.split(' ')
    
    if len(result)==1:
      opcode=result[0]
    if len(result)==2:
      opcode,other=result
      other=other.split(',')
      nr_operands=len(other)
      if nr_operands==1:
        source=other[0]
      elif nr_operands==2:
        source=other[0]
        destination=other[1]
        
    return({'opcode':opcode,'source':source,'destination':destination})
    
  def instruction_type(self,line):
    """blank, label or instruction ?"""
    #delete comments
    line=line.split('#')
    
    line=line[0]
    
    matchobj=re.match(r'^[a-zA-Z]\w+:$',line)
    if matchobj:
      return "label"
      
    matchobj=re.match(r'^\s*$',line)
    if matchobj or line=="":
      return "blank"
    
    return None
    

  def symbol(self):
    """return label or variable"""
    pass
    
  def get_destination(self):
    """return destination"""
    pass
    
  def get_source(self):
    """return source"""
    pass

  def get_opcode(self):
    """return opcode"""
    pass    



class SymbolTable():
  pass
  



class Encoder():
  pass
    
  
class Controller():
  """controls the working of the parser"""
  def __init__(self,file_in,file_out):
    self.file_in=open(file_in,'r')
    self.file_out=open(file_out,'w')
    self.parser=Parser()
    
  def start(self):
    while True:
      line=self.file_in.readline()
      
      if line:
        result=self.parser.parse_line(line)
        print(result)
      else:
        break
        
     
  
if __name__=='__main__':
  file_in=sys.argv[1]
  file_out=sys.argv[2]
  my_controller=Controller(file_in,file_out)
  my_controller.start()
  
  
  

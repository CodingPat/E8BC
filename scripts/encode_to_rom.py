"""write to rom (logisim format 8 bytes per line)"""

import sys

class Controller():

  def __init__(self,file_in,file_out):
    self.file_in=open(file_in,'r')
    self.file_out=open(file_out,'w')
    self.bytes_to_write=[]
    self.bytes_written=0
  
  def write_header(self):
    self.file_out.write("v2.0 raw\n")
   
  
  def write_bytes(self):
    print('Bytes to write :',self.bytes_to_write)
    while len(self.bytes_to_write)>0:
      byte=self.bytes_to_write.pop(0)
      self.file_out.write(byte+' ')
      self.bytes_written+=1
      if self.bytes_written%8==0:
        self.file_out.write('\n')
  
  def start(self):
    self.write_header()
    line=self.file_in.readline()
    while line:
      self.bytes_to_write.extend(line.split())    
      self.write_bytes()
      line=self.file_in.readline()
      
    
  def end(self):
    self.file_in.close()
    self.file_out.close()
    


if __name__=="__main__":
  file_in=sys.argv[1]
  print('file_in :',file_in)
  extension=file_in[-4:]
  file_out=file_in.replace(extension,'.rom')
  print('file_out',file_out)
  my_controller=Controller(file_in,file_out)
  my_controller.start()
  my_controller.end()
  
  
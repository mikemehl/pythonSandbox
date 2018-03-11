import os

testfile = open("test.dat", "wb+")
defaultData = bytes([0xFA,0xCE,0xBE,0xEF])
testfile.write(defaultData)
testfile.close()

key = bytes([0xFF, 0xFF, 0xFF, 0xFF])
newBytes = bytearray()

with open("test.dat", "rb") as theFile:
   fourBytes = theFile.read(4)
   theFile.close()
   for byte in fourBytes:
      newBytes.append(byte ^ key[0])
   newfile = open("out.dat", "wb")
   newfile.write(newBytes)
   newfile.close()
   

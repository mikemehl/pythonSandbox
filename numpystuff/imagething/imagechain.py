import matplotlib.image as img
import pdb
import logging
import multiprocessing as mp

SAMPLE_FILE = 'sample1.jpg'
logging.basicConfig(filename='log.txt', level=logging.INFO)

#Returns a numpy 3d matrix of RGB values.
def getImgData(filename):
   return img.imread(filename)

#Takes output of getImgData and returns a set of all the unique R, G, and B values.
#  aka, all values of 0-255 present in R, G, or B.
#May want to modify this to get unique RBG tuples.
def getUniqueValues(imgdata):
   ret = set()
   size = imgdata.shape
   for pixel in imgdata.flat:
      ret.add(pixel)
   return ret
   
#Same as above, but return unique sequences of a certain length.
#May want to modify this to get unique sequences of RGB tuples.
def getUniqueSeqs(imgdata, length):
   ret = set()
   size = imgdata.shape
   logging.info('Number of pixels: ' + str(len(imgdata.flat)))
   for i in range(0, len(imgdata.flat)):
      if i+length < len(imgdata.flat):
         ret.add(tuple(imgdata.flat[i:i+length]))
      else:
         break
   return ret

def genIndexes(data):
   ret = dict()
   for i in range(0, len(data)):
      ret[str(data)] = i
   return ret

def main():
  data = getImgData(SAMPLE_FILE) 
  vals = getUniqueValues(data)
  seqs = getUniqueSeqs(data, 50)
  #print(seqs)
  return

if __name__ == '__main__':
   main()

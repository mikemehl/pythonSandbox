import matplotlib.image as img
import pdb
import logging
import progressbar
import multiprocessing as mp
from collections import namedtuple
from copy import deepcopy

""" ImageData
    Call with a filename and length passed in to automatically harvest info.
    Then, call getParams to get the info in a UniqueVals namedtuple.
"""


SAMPLE_FILE = 'sample1.jpg'
logging.basicConfig(format='%(asctime)s : %(levelname)6s : %(message)s', level=logging.DEBUG)
UniqueVals = namedtuple('UniqueVals', 'pixels seqs seqlength')

#Class for image operations and data
#class ImageData#######################################################################################
class ImageData:
   def __init__(self, filename):
      try:
         self.filename = filename
         self.data     = self.getImgData(self.filename)
         self.pixels   = self.imgToPixels(self.data)
      except:
         logging.error("Setting up image data failed for " + str(filename))
      return

   def __init__(self, filename, length):
      try:
         self.filename = filename
         self.data     = self.getImgData(self.filename)
         self.pixels   = self.imgToPixels(self.data)
         self.getUniqueData(length)
         self.params   = UniqueVals(pixels = self.values, seqs=self.seqs, seqlength=length)
      except:
         logging.error("Setting up image data failed for " + str(filename))
      return

   def __del__(self):
         pass

   def __enter__(self):
         pass

   def __exit__(self):
         __del__(self)
         return

   #Returns parameters once calculated
   def getParams(self):
      return self.params

   #Returns a numpy 3d matrix of RGB values.
   def getImgData(self, filename):
      try:
         return img.imread(filename)
      except:
         logging.error('Unable to open image: ' + filename)
         return

   #Converts original image data to a list of pixels
   def imgToPixels(self, imgdata):
      print("Converting image format...")
      return [tuple(imgdata.flat[x:x+3]) for x in range(0,len(imgdata.flat),3)]

   #Takes output of imgToPixels and returns a set of all the unique RGB values.
   def getUniqueValues(self):
      ret = set()
      logging.info("Number of pixels: " + str(len(self.pixels)))
      print("Reading unique pixels...")
      with progressbar.ProgressBar(max_value = len(self.pixels), redirect_stdout=True) as bar:
              k = 0
              for pixel in self.pixels:
                 ret.add(tuple(pixel))
                 k += 1
                 bar.update(k)
      return ret
   
   #Same as above, but return unique sequences of a certain length.
   def getUniqueSeqs(self, length):
      ret = set()
      logging.info('Number of pixels: ' + str(len(self.pixels)))
      print("Reading unique sequences...")
      with progressbar.ProgressBar(max_value = len(self.pixels), redirect_stdout=True) as bar:
              k = 0
              for i in range(0, len(self.pixels)):
                 if i+length < len(self.pixels):
                    ret.add(tuple(self.pixels[i:i+length]))
                    k += 1
                    bar.update(k)
                 else:
                    break
      return ret

   def getUniqueData(self, length):
      self.values = self.getUniqueValues()
      self.seqs   = self.getUniqueSeqs(length)
      return
###################################################################################################
def main():
  img  = ImageData(SAMPLE_FILE, 50) 
  dude = img.getParams()
  logging.debug(list(dude.pixels)[5])
  logging.debug(list(dude.seqs)[5])
  return

if __name__ == '__main__':
   main()

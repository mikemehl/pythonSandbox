""" IDEA:
      We want our Markov Chain to look at the last n pixels to decided the
      next pixel to place. But what if that sequence doesn't appear in the
      Markov Chain already?
      Try defining a metric on the space of n-tuples of RGB values. Then, 
      if the sequence isn't in our chain, find the closest sequence!
"""

import numpy as np
from ImageData import ImageData
from ImageData import UniqueVals
from ImageData import SAMPLE_FILE
from math import sqrt
import logging
import progressbar

MAT_FILE = 'markovmtx.dat'
MAX_ENTRY = (2**8)-1
MEM_LIMIT  = 15
TYPE_SIZE = 1

class MarkovMatrix:
   def __init__(self, img):
      assert(type(img) is ImageData)
      self.xi, self.yi = self.getMatrixDicts(img.seqs, img.values)
      bneeded = len(self.xi)*len(self.yi)*TYPE_SIZE
      gneeded = bneeded*10e-9
      if gneeded > MEM_LIMIT:
        logging.debug('MEM_LIMIT: ' + str(MEM_LIMIT))
        logging.debug('Required size: ' + str(gneeded))
        raise OverflowError('Max memory limit exceeded.')
      logging.debug('X Length: ' + str(len(self.xi)))
      logging.debug('Y Length: ' + str(len(self.yi)))
      logging.debug('Size needed: ' + str(bneeded) + ' bytes, approximately ' + str(gneeded) + ' gigabytes.')
      self.mat = np.memmap(MAT_FILE, dtype='uint8', mode='w+', shape=(len(self.xi),len(self.yi)))
      self.addValsToMatrix(img)
      return

   def getMatrixDicts(self, xvals, yvals):
       xindexes = dict() 
       yindexes = dict()
       print("Assigning x indexes...")
       with progressbar.ProgressBar(max_value = len(xvals), redirect_stdout=True) as bar:
               i = 0
               for val in xvals:
                   xindexes[val]=i
                   i += 1
                   bar.update(i)
       print("Assigning y indexes...")
       with progressbar.ProgressBar(max_value = len(yvals), redirect_stdout=True) as bar:
               j = 0
               for val in yvals:
                   yindexes[val]=j
                   j += 1
                   bar.update(j)
       logging.debug('Xlen: ' + str(i))
       logging.debug('Ylen: ' + str(j))
       return xindexes, yindexes

#Use the output of getMatrixDicts and passed in matrix to fill out the matrix.
#Returns number of values processed (matrix is filled with instances, not probability).
#  xi, yi - dictionary for index lookup of matrix
#  img    - ImageData holding image info
   def addValsToMatrix(self, img):
       print("Adding values to transition matrix...")
       try:
           assert(type(img) is ImageData)
           count = 0
           pixels = img.pixels
           length = img.length
           with progressbar.ProgressBar(max_value = len(pixels), redirect_stdout=True) as bar:
               k = 0
               for i in range(0,len(pixels)):
                   if i+length+1 < len(pixels):
                       seq = tuple(pixels[i:i+length])
                       nxt = tuple(pixels[i+length+1])
                       xindex = self.xi[seq]
                       yindex = self.yi[nxt]
                       logging.debug(str(nxt) + ' has index ' + str(yindex))
                       assert(xindex < self.mat.shape[0])
                       assert(yindex < self.mat.shape[1])
                       if self.mat[xindex][yindex] < MAX_ENTRY:
                           #logging.info('Incrementing ('+ str(xindex)+', '+str(yindex)+')')
                           self.mat[xindex][yindex] += 1
                       else:
                           logging.critical('MAX SIZE: ' + str(self.mat[xindex][yindex]))
                           raise ValueError('Entry exeeded max size of entry!')
                       count += 1
                       k += 1
                       bar.update(k)
                   else: 
                       break
       except:
           logging.error('Unable to add values to matrix.')
           assert(False)
       return count

#Distance between two sequences.
#Flatten sequences and find euclidean distance.
   def metric(self, seq1, seq2):
      try: 
           assert(len(seq1) == len(seq2))
           sub = [None]*len(seq1)
           for i in range(0, len(seq1)):
               sub[i] = (int(seq1[i]) - int(seq2[i]))
           sub = [x**2 for x in sub]
           return sqrt(sum(sub))
      except:
           print("Unable to determine metric.")
           raise ValueError("Bad parameters passed to metric().")

# Given input seed, find next pixel to place.
   def oneStep(self, seed):
       try:
           #Verify length of seed.
           assert(len(seed) is img.length)
           if seed in img.seqs:
               #Great! Use that value to determine probability.
           else:
               #Find the closet value in the set
           #Determine probabilities.
           #Flip a coin.
           #Return what should be next.
       except:
           logging.critical('oneStep failed.')
           assert(False)
       return

def main():
    img    = ImageData(SAMPLE_FILE, 200)
    dude   = img.getParams()
    mtx = MarkovMatrix(img)
    #print(metric(np.array([1,2,3]),np.array([4,5,6])))
    return
if __name__ == "__main__":
    main()


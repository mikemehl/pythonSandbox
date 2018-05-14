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
import logging

MAT_FILE = 'markovmtx.dat'

def getMatrixDicts(xvals, yvals):
    xindexes = dict() 
    yindexes = dict()
    i = 0
    for val in xvals:
        xindexes[val]=i
    j = 0
    for val in yvals:
        yindexes[val]=j
    return xindexes, yindexes

#Use the output of getMatrixDicts and passed in matrix to fill out the matrix.
#Returns number of values processed (matrix is filled with instances, not probability).
def addValsToMatrix(mat, xi, yi):
    return

def main():
    img    = ImageData(SAMPLE_FILE, 50)
    dude   = img.getParams()
    xi, yi = getMatrixDicts(dude.seqs, dude.pixels)
    logging.debug('X Length: ' + str(len(xi)))
    logging.debug('Y Length: ' + str(len(yi)))
    #Oh boy, this thing is huge. Use int8 for your matrix to save space. 
    #Don't forget to check for overflow later!
    mat = np.memmap(MAT_FILE, dtype='int8', mode='w+', shape=(len(xi),len(yi)))
    return
if __name__ == "__main__":
    main()


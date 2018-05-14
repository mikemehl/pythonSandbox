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
import progressbar

MAT_FILE = 'markovmtx.dat'
MAX_ENTRY = 2**32-1


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
#  mat    - reference to memory mapped matrix
#  xi, yi - dictionary for index lookup of matrix
#  img    - ImageData holding image info
#  length - length of sequences to consider
def addValsToMatrix(mat, xi, yi, img):
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
                    xindex = xi[seq]
                    yindex = yi[nxt]
                    if mat[xindex][yindex] < MAX_ENTRY:
                        mat[xindex][yindex] += 1
                    else:
                        logging.critical('MAX SIZE: ' + str(mat[xindex][yindex]))
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

def main():
    img    = ImageData(SAMPLE_FILE, 750)
    dude   = img.getParams()
    xi, yi = getMatrixDicts(dude.seqs, dude.pixels)
    logging.debug('X Length: ' + str(len(xi)))
    logging.debug('Y Length: ' + str(len(yi)))
    #Oh boy, this thing is huge. Use int8 for your matrix to save space. 
    #Don't forget to check for overflow later!
    mat = np.memmap(MAT_FILE, dtype='uint32', mode='w+', shape=(len(xi),len(yi)))
    mat.flush()
    addValsToMatrix(mat, xi, yi, img)
    return
if __name__ == "__main__":
    main()


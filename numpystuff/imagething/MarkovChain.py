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
MAX_ENTRY = (2**8)-1
MEM_LIMIT  = 15
TYPE_SIZE = 1


def getMatrixDicts(xvals, yvals):
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
                        #logging.info('Incrementing ('+ str(xindex)+', '+str(yindex)+')')
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
    img    = ImageData(SAMPLE_FILE, 200)
    dude   = img.getParams()
    xi, yi = getMatrixDicts(dude.seqs, dude.pixels)
    bneeded = len(xi)*len(yi)*TYPE_SIZE
    gneeded = bneeded*10e-9
    if gneeded > MEM_LIMIT:
      logging.debug('MEM_LIMIT: ' + str(MEM_LIMIT))
      logging.debug('Required size: ' + str(gneeded))
      raise OverflowError('Max memory limit exceeded.')
    logging.debug('X Length: ' + str(len(xi)))
    logging.debug('Y Length: ' + str(len(yi)))
    logging.debug('Size needed: ' + str(bneeded) + ' bytes, approximately ' + str(gneeded) + ' gigabytes.')
    #Don't forget to check for overflow later!
    mat = np.memmap(MAT_FILE, dtype='uint8', mode='w+', shape=(len(xi),len(yi)))
    addValsToMatrix(mat, xi, yi, img)
    return
if __name__ == "__main__":
    main()


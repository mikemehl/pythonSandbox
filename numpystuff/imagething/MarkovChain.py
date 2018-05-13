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

def setupMatrix(xvals, yvals):
    xindexes = dict() 
    yindexes = dict()
    i = 0
    for val in xvals:
        xindexes[val]=i
    j = 0
    for val in yvals:
        yindexes[val]=j
    return np.zeros((len(xvals),len(yvals))), xindexes, yindexes

def main():
    img = ImageData(SAMPLE_FILE, 50)
    dude = img.getParams()
    mat, xi, yi = setupMatrix(dude.seqs, dude.pixels)
    print("Setup matrix.")
    print(mat[0][0])
    return
if __name__ == "__main__":
    main()


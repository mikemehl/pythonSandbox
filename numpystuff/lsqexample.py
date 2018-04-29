import numpy as np

DATAFILE = 'data.txt'
MAX_DEGREE = 5

def readData():
   xdata = []
   ydata = []
   with open(DATAFILE, 'r') as indata:
      for line in indata:
              polydata = []
              splitup = line.split()
              ydata.append(float(splitup[1]))
              for i in range(0, MAX_DEGREE+1):
                      polydata.append(pow(float(splitup[0]), i))
              xdata.append(polydata)
   mat  = np.array(xdata)
   vect = np.array(ydata)
#Do a QR? Use LSQ? your call!
   return mat, vect

def qrlsq(xdata, ydata):
   q, r = np.linalg.qr(xdata)
   return np.linalg.solve(r, np.matmul(q.transpose(), ydata))

def classiclsq(xdata, ydata):
   A = np.matmul(xdata.transpose(), xdata)
   b = np.matmul(xdata.transpose(), ydata)
   return np.linalg.solve(A, b)


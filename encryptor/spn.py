import random
import pdb

samplebytes = bytes([0x01,0x02,0x03,0x04])
          # 0   1   2   3  4   5   6   7   8   9   10  11  12  13  14  15
sub     = ( 9, 11, 12,  4, 1,  7,  2, 15, 10, 13,  5,  14,  8,  3,  0,  6)
invsub  = (14,  4,  6, 13, 3, 10, 15,  5, 12,  0,  8,   1,  2,  9, 11,  7) 

perm    = (1, 2, 0, 3)
invperm = (2, 0, 1, 3)

hi_mask = 0b11110000
lo_mask = 0b00001111

def substitution(halfbyte):
    return sub[halfbyte]

def permutation(fourbytes):
    newbytes = [fourbytes[i] for i in perm]
    return bytes(newbytes) 

# Expects: 
#         * fourbytes as a bytes object with four members
#         * key as a list of ints
def one_stage_enc(fourbytes, key):
    newbytes = []
    for onebyte in fourbytes:
        #pdb.set_trace()
        val = int(onebyte)
        hi = (val & hi_mask) >> 4
        lo = (val & lo_mask)
        newhi = substitution(hi)
        newlo = substitution(lo)
        newval = (newhi << 4) | newlo
        newbytes.append(newval)
    for i in range(0, len(key)):
        newbytes[i] = newbytes[i]^int(key[i])
    return permutation(bytes(newbytes))
        

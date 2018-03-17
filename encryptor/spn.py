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

def inv_substitution(halfbyte):
    return invsub[halfbyte]

def permutation(fourbytes):
    newbytes = [fourbytes[i] for i in perm]
    return bytes(newbytes) 

def inv_permutation(fourbytes):
    newbytes = [fourbytes[i] for i in invperm]
    return bytes(newbytes) 

#########################################################
# one_stage_enc
#########################################################
# Expects: 
#         * fourbytes as a bytes object with four members
#         * key as a list of ints
# Returns:
#         * four bytes
def one_stage_enc(fourbytes, key):
    newbytes = []
    for onebyte in fourbytes:
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
        
#########################################################
# one_stage_dec
#########################################################
# Expects: 
#         * fourbytes as a bytes object with four members
#         * key as a list of ints
# Returns:
#         * four bytes
def one_stage_dec(fourbytes, key):
    newbytes = [None]*len(key)
    for i in range(0, len(key)):
        newbytes[i] = int(fourbytes[i])^int(key[i])
    invbytes = inv_permutation(bytes(newbytes))
    newbytes = []
    for onebyte in invbytes:
        val = int(onebyte)
        hi = (val & hi_mask) >> 4
        lo = (val & lo_mask)
        newhi = inv_substitution(hi)
        newlo = inv_substitution(lo)
        newval = (newhi << 4) | newlo
        newbytes.append(newval)
    return bytes(newbytes)

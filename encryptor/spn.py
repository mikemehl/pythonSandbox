import random
import pdb
import multiprocessing as mp

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
    newbytes = []
    invbytes = inv_permutation(bytes(fourbytes))
    xoredbytes = [None]*len(fourbytes)
    for i in range(0, len(key)):
        xoredbytes[i] = int(invbytes[i])^int(key[i])
    for onebyte in xoredbytes:
        val = int(onebyte)
        hi = (val & hi_mask) >> 4
        lo = (val & lo_mask)
        newhi = inv_substitution(hi)
        newlo = inv_substitution(lo)
        newval = (newhi << 4) | newlo
        newbytes.append(newval)
    return bytes(newbytes)

#########################################################
# one_round_enc
#########################################################
# Expects: 
#         * data as a list of ints
#         * key as a list of four ints
#         * stages as an int
# Returns:
#         * encrypted data as list of bytes objects 
def one_round_enc(data, key, stages):
    bin_data = bytes(data)
    words = [bin_data[i:(i+4)] for i in range(0, len(data), 4)]
    newwords = []
    currword = bytes(4)
    for word in words:
        currword = word
        for i in range(0, stages):
            currword = one_stage_enc(currword, key)
        newwords.append(currword)
    return b''.join(newwords)

#########################################################
# one_round_dec
#########################################################
# Expects: 
#         * data as a list of ints
#         * key as a list of four ints
#         * stages as an int
# Returns:
#         * decrypted data as list of bytes objects 
def one_round_dec(data, key, stages):
    bin_data = bytes(data)
    words = [bin_data[i:(i+4)] for i in range(0, len(data), 4)]
    newwords = []
    currword = bytes(4)
    for word in words:
        currword = word
        for i in range(0, stages):
            currword = one_stage_dec(currword, key)
        newwords.append(currword)
    return b''.join(newwords)

#########################################################
# encrypt 
#########################################################
# Expects: 
#         * data as bytes
#         * key as a list of four bytes 
#         * stages as an int
# Returns:
#         * decrypted data as a bytestring
def encrypt(data, key, stages):
    while len(data)%4 != 0:
        data.append(0x00)
    key_int = [int(key[i]) for i in range(0,4)]
    encrypted = []
    for i in range(0, len(data), 4):
        key_int = key_int[1:] + key_int[:1]
        encrypted.append(one_round_enc(data[i:i+4], key_int, stages))
        print(key_int)
    return b''.join(encrypted)

#########################################################
# decrypt 
#########################################################
# Expects: 
#         * data as bytes
#         * key as a list of four bytes 
#         * stages as an int
# Returns:
#         * decrypted data as a bytestring
def decrypt(data, key, stages):
    key_int = [int(key[i]) for i in range(0,4)]
    decrypted = []
    for i in range(0, len(data), 4):
        key_int = key_int[1:] + key_int[:1]
        decrypted.append(one_round_dec(data[i:i+4], key_int, stages))
        print(key_int)
    return b''.join(decrypted)

#########################################################
# one_round_enc_args
#########################################################
# Expects: 
#         * packed data
# Returns:
#         * encrypted data
def one_round_enc_args(packed):
    return one_round_enc(packed[0], packed[1], packed[2])

#########################################################
# one_round_dec_args
#########################################################
# Expects: 
#         * packed data
# Returns:
#         * encrypted data
def one_round_dec_args(packed):
    return one_round_dec(packed[0], packed[1], packed[2])

#########################################################
# encrypt_multi 
#########################################################
# Expects: 
#         * data as bytes
#         * key as a list of four bytes 
#         * stages as an int
# Returns:
#         * decrypted data as a bytestring
def encrypt_multi(data, key, stages):
    while len(data)%4 != 0:
        data.append(0x00)
    key_int = [int(key[i]) for i in range(0,4)]
    args = []
    for i in range(0, len(data), 4):
        newlist = [None]*3
        newlist[0] = data[i:i+4]
        newlist[1] = key_int[1:] + key_int[:1]
        newlist[2] = stages
        args.append(newlist)
    #encrypted.append(one_round_enc(data[i:i+4], key_int, stages))
    pool = mp.Pool(processes=4)
    encrypted = pool.map(one_round_enc_args, args)
    return b''.join(encrypted)

#########################################################
# decrypt_multi 
#########################################################
# Expects: 
#         * data as bytes
#         * key as a list of four bytes 
#         * stages as an int
# Returns:
#         * decrypted data as a bytestring
def decrypt_multi(data, key, stages):
    while len(data)%4 != 0:
        data.append(0x00)
    key_int = [int(key[i]) for i in range(0,4)]
    args = []
    for i in range(0, len(data), 4):
        newlist = [None]*3
        newlist[0] = data[i:i+4]
        newlist[1] = key_int[1:] + key_int[:1]
        newlist[2] = stages
        args.append(newlist)
    pool = mp.Pool(processes=4)
    decrypted = pool.map(one_round_dec_args, args)
    return b''.join(decrypted)


#########################################################
# encrypt_file 
#########################################################
def encrypt_file(fileName, outName, key, stages):
    inFile = open(fileName, 'rb')
    outFile = open(outName, 'wb')
    inData = theFile.read(512)
    outData = []
    while inData:
        outFile.write(encrypt_multi(inData, key, stages))
        inData = inFile.read(512)
    
#########################################################
# decrypt_file 
#########################################################
def decrypt_file(fileName, outName, key, stages):
    inFile = open(fileName, 'rb')
    outFile = open(outName, 'wb')
    inData = theFile.read(512)
    outData = []
    while inData:
        outFile.write(decrypt_multi(inData, key, stages))
        inData = inFile.read(512)

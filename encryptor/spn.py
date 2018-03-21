import random
import pdb
import multiprocessing as mp
import logging
import os
import shutil
import progressbar

log = logging.getLogger()
log.setLevel(logging.DEBUG)
logging.disable(logging.DEBUG)

samplebytes = bytes([i for i in range(0,64)])
          # 0   1   2   3  4   5   6   7   8   9   10  11  12  13  14  15
SUB     = ( 9, 11, 12,  4, 1,  7,  2, 15, 10, 13,  5,  14,  8,  3,  0,  6)
INVSUB  = (14,  4,  6, 13, 3, 10, 15,  5, 12,  0,  8,   1,  2,  9, 11,  7) 

          # 0   1   2   3  4   5   6   7   8   9   10  11  12  13  14  15
PERM    = ( 1,  2,  0,  7, 14, 9,  8,  3,  6,  4,   5, 10, 13, 11, 15, 12)
INVPERM = ( 2,  0,  1,  7,  9,10,  8,  3,  6,  5,  11, 13, 15, 12,  4, 14)

HI_MASK = 0b11110000
LO_MASK = 0b00001111

BLOCK_LENGTH = 16
KEY_LENGTH = BLOCK_LENGTH

NONCE = 0xAB38D39FEBC0EF160000000000000000

def substitution(halfbyte):
    return SUB[halfbyte]

def inv_substitution(halfbyte):
    return INVSUB[halfbyte]

def permutation(sixteenbytes):
    newbytes = [sixteenbytes[i] for i in PERM]
    return bytes(newbytes) 

def inv_permutation(sixteenbytes):
    newbytes = [sixteenbytes[i] for i in INVPERM]
    return bytes(newbytes) 

#########################################################
# one_stage_enc
#########################################################
# Expects: 
#         * sixteenbytes as a bytes object with sixteen members
#         * key as a list of ints
# Returns:
#         * sixteen bytes
def one_stage_enc(sixteenbytes, key):
    assert len(sixteenbytes) == BLOCK_LENGTH
    assert len(key) == KEY_LENGTH
    newbytes = []
    for onebyte in sixteenbytes:
        val = int(onebyte)
        hi = (val & HI_MASK) >> 4
        lo = (val & LO_MASK)
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
#         * sixteenbytes as a bytes object with sixteen members
#         * key as a list of ints
# Returns:
#         * four bytes
def one_stage_dec(sixteenbytes, key):
    assert len(sixteenbytes) == BLOCK_LENGTH
    assert len(key) == KEY_LENGTH
    newbytes = []
    invbytes = inv_permutation(bytes(sixteenbytes))
    xoredbytes = [None]*len(sixteenbytes)
    for i in range(0, len(key)):
        xoredbytes[i] = int(invbytes[i])^int(key[i])
    for onebyte in xoredbytes:
        val = int(onebyte)
        hi = (val & HI_MASK) >> 4
        lo = (val & LO_MASK)
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
    assert len(key) == KEY_LENGTH
    bin_data = bytes(data)
    words = [bin_data[i:(i+16)] for i in range(0, len(data), 16)]
    newwords = []
    currword = bytes(16)
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
    assert len(key) == KEY_LENGTH
    bin_data = bytes(data)
    words = [bin_data[i:(i+16)] for i in range(0, len(data), 16)]
    newwords = []
    currword = bytes(16)
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
    assert len(key) == KEY_LENGTH
    while len(data)%16 != 0:
        data.append(0x00)
    key_int = [int(key[i]) for i in range(0,len(key))]
    encrypted = []
    for i in range(0, len(data), 16):
        key_int = key_int[1:] + key_int[:1]
        encrypted.append(one_round_enc(data[i:i+16], key_int, stages))
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
    assert len(key) == KEY_LENGTH
    key_int = [int(key[i]) for i in range(0,16)]
    decrypted = []
    for i in range(0, len(data), 16):
        key_int = key_int[1:] + key_int[:1]
        decrypted.append(one_round_dec(data[i:i+16], key_int, stages))
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
# encrypt_file 
#########################################################
def encrypt_file(fileName, outName, key, stages):
    inFile = open(fileName, 'rb')
    outFile = open(outName, 'wb')
    pool = mp.Pool(processes=4)
    outData = []
    inData = inFile.read(512)
    while inData:
        while len(inData)%16 != 0:
            inData += bytes(1)
        key_int = [int(key[i]) for i in range(0,len(key))]
        args = []
        for i in range(0, len(inData), 16):
            newlist = [None]*3
            newlist[0] = inData[i:i+16]
            newlist[1] = key_int[1:] + key_int[:1]
            newlist[2] = stages
            args.append(newlist)
        outFile.write(b''.join(pool.map(one_round_enc_args, args)))
        inData = inFile.read(512)
    inFile.close()
    outFile.close()
    
#########################################################
# decrypt_file 
#########################################################
def decrypt_file(fileName, outName, key, stages):
    inFile = open(fileName, 'rb')
    outFile = open(outName, 'wb')
    pool = mp.Pool(processes=4)
    outData = []
    inData = inFile.read(512)
    while inData:
        while len(inData)%16 != 0:
            inData += bytes(1)
        key_int = [int(key[i]) for i in range(0,len(key))]
        args = []
        for i in range(0, len(inData), 16):
            newlist = [None]*3
            newlist[0] = inData[i:i+16]
            newlist[1] = key_int[1:] + key_int[:1]
            newlist[2] = stages
            args.append(newlist)
        outFile.write(b''.join(pool.map(one_round_dec_args, args)))
        inData = inFile.read(512)
    inFile.close()
    outFile.close()

#########################################################
# encrypt_file_counter
#########################################################
def encrypt_file_counter(fileName, outName, key, stages):
    counter = int(NONCE)
    inFile = open(fileName, 'rb')
    outFile = open(outName, 'wb')
    pool = mp.Pool(processes=4)
    outData = []
    inData = inFile.read(512)
    while inData:
        while len(inData)%16 != 0:
            inData += bytes(1)
        key_int = [int(key[i]) for i in range(0,len(key))]
        args = []
        for i in range(0, len(inData), 16):
            newlist = [None]*3
            newlist[0] = int.to_bytes(counter, 16, byteorder='big')
            newlist[1] = key_int[1:] + key_int[:1]
            newlist[2] = stages
            args.append(newlist)
            counter += 1
        result = b''.join(pool.map(one_round_enc_args, args))
        towrite = bytes([result[i]^inData[i]  \
                        for i in range(0, len(inData))])
        outFile.write(towrite)
        inData = inFile.read(512)
    inFile.close()
    outFile.close()
    
#########################################################
# encrypt_directory
#########################################################
def encrypt_directory(directory, key):
    currdir = os.getcwd()
    os.chdir(directory + '/..')
    try:
        shutil.copytree(directory, directory + '_ENCRYPTED')
    except:
        print("~~~Unable to complete operation~~~")
    os.chdir(directory + '_ENCRYPTED')
    print("Grabbing filenames...")
    dudes = [os.path.join(d, x) for d, dirx, files in os.walk(os.getcwd()) for x in files]
    print('Encrypting...')
    with progressbar.ProgressBar(max_value=len(dudes), redirect_stdout=True) as bar:
        i = 0
        for dude in dudes:
            print('Encrypting ' + os.path.basename(dude))
            encrypt_file_counter(dude, dude+'_ENCRYPTED', key, 10)
            os.unlink(dude)
            shutil.move(dude+'_ENCRYPTED', dude)
            i += 1
            bar.update(i)
    print('Finished.')
    os.chdir(currdir)
    return

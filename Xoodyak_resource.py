
from projectq.ops import H, CNOT, Measure, Toffoli, X, All , Swap
from projectq import MainEngine
from projectq.backends import ResourceCounter, ClassicalSimulator
from projectq.meta import Loop, Compute, Uncompute, Control

def Xodyak(eng, m_value, len):

    s = eng.allocate_qureg(384)
    result = eng.allocate_qureg(128)

    len_left = 0

    if (len != 0):
        if(len % 128 == 0):
            l = int(len / 128)
        else :
            l = int(len / 128) + 1
    else:
        l = 1

    if (len < 128):
        #Round_constant_XOR(eng, s, m_value, len)
        print('len < 128')
    else:
        #Round_constant_XOR(eng, s, m_value, 128)
        len_left = len-128

    #Absorb
    for number in range(l):
        if(number==0):
            if(len_left > 0):
                X | s[128]
                X | s[376]
            else:
                X | s[len]
                X | s[376]
        else:
            Permutation(eng, s)

            if (len_left < 128):
                M = eng.allocate_qureg(len_left)
                #Round_constant_XOR2(eng, M, m_value, len_left, number)
                Message_XOR(eng, s, M, len_left)
                X | s[len_left]
            else:
                M = eng.allocate_qureg(128)
                #Round_constant_XOR2(eng, M, m_value, 128, number)
                Message_XOR(eng, s, M, 128)
                X | s[128]
                len_left = len_left - 128

    # Squeeze
    Permutation(eng, s)

    #print('\nHash result(Low part)')

    for i in range(128):
        CNOT | (s[127 - i], result[127 - i])
    #print_state(eng, result)

    X | s[0]
    Permutation(eng, s)

    #print('\nHash result(Hight part)')
    #print_state(eng, s)

def Permutation(eng, input):

    rc =  (0x00000058, 0x00000038, 0x000003C0, 0x000000D0, 0x00000120, 0x00000014, 0x00000060, 0x0000002C, 0x00000380, 0x000000F0, 0x000001A0, 0x00000012)

    a0 = []
    a1 = []
    a2 = []

    # divide lane

    for i in range(128):
        a0.append(input[i])
        a1.append(input[i + 128])
        a2.append(input[i + 256])

    for number in range(12):
        p = eng.allocate_qureg(128)

        # Compute p
        for i in range(128):
            CNOT | (a0[i], p[i])
            CNOT | (a1[i], p[i])
            CNOT | (a2[i], p[i])

        # Complete delta
        Rotate_xor(eng, p, a0)
        Rotate_xor(eng, p, a1)
        Rotate_xor(eng, p, a2)

        #P_west(eng, a1, a2)

        Round_constant_XOR(eng, input, rc[number], 32) # Change to iteration number (i)

        b0 = eng.allocate_qureg(128)
        b1 = eng.allocate_qureg(128)

        All(X) | a1
        Toffoli_128(eng, a1, a2, b0)
        All(X) | a1 #reverse

        All(X) | a2
        Toffoli_128(eng, a2, a0, b1)
        All(X) | a2  # reverse

        All(X) | a0
        Toffoli_128(eng, a0, a1, a2)
        All(X) | a0  # reverse

        CNOT_128(eng, b0, a0)
        CNOT_128(eng, b1, a1)

        #P_east(eng, a1, a2)



def Rotate_xor(eng, p, a):

    for i in range(32):
        CNOT | (p[96+i], a[(5+i) % 32])
        CNOT | (p[96 + i], a[(14 + i) % 32])
        CNOT | (p[i], a[32+ ((5 + i) % 32)])
        CNOT | (p[i], a[32 + ((14 + i) % 32)])
        CNOT | (p[32+i], a[64 + ((5 + i) % 32)])
        CNOT | (p[32+i], a[64 + ((14 + i) % 32)])
        CNOT | (p[64 + i], a[96 + ((5 + i) % 32)])
        CNOT | (p[64 + i], a[96 + ((14 + i) % 32)])

def Toffoli_128(eng, a, b, c):
    for i in range(128):
        Toffoli | (a[i], b[i], c[i])

def CNOT_128(eng, a, b):
    for i in range(128):
        CNOT | (a[i], b[i])

def Swap_32(eng, a, b):
    for i in range(32):
        Swap | (a[i], b[i])

def P_west(eng, a1, a2):

    Swap_32(eng, a1[96:128], a1[64:96])
    Swap_32(eng, a1[64:96], a1[32:64])
    Swap_32(eng, a1[32:64], a1[0:32])

    for i in range(11):
        for j in range(31):
            Swap | (a2[31-j], a2[30-j])
            Swap | (a2[63 - j], a2[62 - j])
            Swap | (a2[95 - j], a2[94 - j])
            Swap | (a2[127 - j], a2[126 - j])

def P_east(eng, a1, a2):

    for j in range(31):
        Swap | (a1[31-j], a1[30-j])
        Swap | (a1[63 - j], a1[62 - j])
        Swap | (a1[95 - j], a1[94 - j])
        Swap | (a1[127 - j], a1[126 - j])

    Swap_32(eng, a2[96:128], a2[64:96])
    Swap_32(eng, a2[64:96], a2[32:64])
    Swap_32(eng, a2[32:64], a2[0:32])

    Swap_32(eng, a2[96:128], a2[64:96])
    Swap_32(eng, a2[64:96], a2[32:64])
    Swap_32(eng, a2[32:64], a2[0:32])

    for i in range(8):
        for j in range(31):
            Swap | (a2[31-j], a2[30-j])
            Swap | (a2[63 - j], a2[62 - j])
            Swap | (a2[95 - j], a2[94 - j])
            Swap | (a2[127 - j], a2[126 - j])

def Round_constant_XOR(eng, k, rc, bit):
    for i in range(bit):
        if(rc >> i & 1):
             X | k[i]

def Round_constant_XOR2(eng, k, rc, bit, block_number):
    for i in range(bit):
        if((rc >> (128 * block_number) + i) & 1):
             X | k[i]

def Message_XOR(eng, k, rc, bit):
    for i in range(bit):
        CNOT | (rc[i], k[i])

def print_state(eng, x):

    All(Measure) | x
    for i in range(128):
        print(int(x[127-i]), end='')
        if((i+1) % 32 == 0):
            print(" ", end='')
    print('\n')

Resource = ResourceCounter()
eng = MainEngine(Resource)
Xodyak(eng, 0x201f1e1d1c1b1a191817161514131211100f0e0d0c0b0a09080706050403020100, 256)
print('\n')
print(Resource)
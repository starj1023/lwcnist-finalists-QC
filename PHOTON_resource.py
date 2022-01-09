
from projectq.ops import H, CNOT, Measure, Toffoli, X, All , Swap
from projectq import MainEngine
from projectq.backends import ResourceCounter, ClassicalSimulator
from projectq.meta import Loop, Compute, Uncompute, Control


def Photon(eng, M_value, len):

    IV = eng.allocate_qureg(256)
    result = eng.allocate_qureg(128)

    if(len==0):
        X | IV[253]

        phton(eng, IV)
        for i in range(128):
            CNOT | (IV[127 - i], result[127 - i])
        #print_state(eng, result)

        phton(eng, IV)
        #print_state(eng, IV)

        return

    if(len <= 128):
        if (len<128):
            #Message_XOR(eng, IV, M_value, len)
            X | IV[len]
            X | IV[253]
        else:
            #Message_XOR(eng, IV, M_value, len)
            X | IV[254]

        phton(eng, IV)
        for i in range(128):
            CNOT | (IV[127 - i], result[127 - i])
        #print_state(eng, result)

        phton(eng, IV)
        #print_state(eng, IV)

    else:
        c0 = 2
        #Message_XOR(eng, IV, M_value, 128)  # 128~~ --> M1
        m_len = len-128
        M = eng.allocate_qureg(m_len)
        #Message_XOR2(eng, M, M_value, m_len)

        if (int(m_len % 32) == 0):
            D_i = int(m_len / 32)
            c0 = 1
        else:
            D_i = int(m_len / 32) + 1

        for i in range(D_i):

            phton(eng, IV)
            if (i == D_i - 1):

                if(int(m_len%32)!= 0 ):
                    for j in range(int(m_len % 32)):
                        CNOT | (M[32*i+j], IV[j])
                    X | IV[int(m_len % 32)]
                else:
                    for j in range(32):
                        CNOT | (M[32 * i + j], IV[j])
            else:
                for j in range(32):
                    CNOT | (M[32*i+j], IV[j])

        if(c0 == 1):
            X | IV[253]
        else:
            X | IV[254]

        phton(eng, IV)
        for i in range(128):
            CNOT | (IV[127 - i], result[127 - i])
        #print_state(eng, result)

        phton(eng, IV)
        #print_state(eng, IV)

def phton(eng, x):

    c = (2, 4, 2, 11, 2, 8, 5, 6, 12, 9, 8, 13, 7, 7, 5, 2, 4, 4, 13, 13, 9, 4, 13, 9, 1, 6, 5, 1, 12, 13, 15, 14,
         15, 12, 9, 13, 14, 5, 14, 13, 9, 14, 5, 15, 4, 12, 9, 6, 12, 2, 2, 10, 3, 1, 1, 14, 15, 1, 13, 10, 5, 10, 2, 3)

    for p in range(12):
        AddConstant(eng, x, p)
        Subcell(eng, x)
        #Shiftrow(eng, x)
        result = eng.allocate_qureg(256)
        Mixcolumn(eng, x, result, c, p)
        #Swap_result(eng, x, result)

def Mixcolumn(eng, x, result, c, p):

    for j in range(8):
        for i in range(8):
            for z in range(8):
                Constant_Multiplication(eng, x[32 * z + 4 * j:32 * z + 4 * j + 4], result[32 * i + 4 * j:32 * i + 4 * j + 4], c[8 * i + z])

def AddConstant(eng, x, i):

    RC = (1, 3, 7, 14, 13, 11, 6, 12, 9, 2, 5, 10)
    IC = (0, 1, 3, 7, 15, 14, 12, 8)

    for j in range(8):
        Round_constant_XOR(eng, x[32*j:32*j+4], RC[i])
        Round_constant_XOR(eng, x[32*j:32*j+4], IC[j])

def Round_constant_XOR(eng, k, rc):
    for i in range(4):
        if (rc >> i & 1):
            X | k[i]

def Subcell(eng, x):

    for i in range(64):
        SBox_new(eng, x[4*i:4*i+4])

def SBox_new(eng, x):

    f0 = x[2]
    f1 = x[3]
    f2 = x[1]
    f3 = x[0]

    CNOT | (f0, f2)
    Toffoli | (f2, f0, f1)
    Toffoli | (f2, f1, f0)
    Toffoli | (f3, f0, f2)
    CNOT | (f1, f2)
    X | (f3)
    X | (f1)
    CNOT | (f2, f0)
    CNOT | (f3, f2)
    CNOT | (f1, f3)
    Toffoli | (f2, f0, f1)

    #Swap | (x[1], x[2])
    #Swap | (x[2], x[3])

def Shiftrow(eng, x):

    for j in range(4):
        for i in range(31):
            Swap | (x[32 + i], x[33 + i])
    for j in range(8):
        for i in range(31):
            Swap | (x[64 + i], x[65 + i])
    for j in range(12):
        for i in range(31):
            Swap | (x[96 + i], x[97 + i])
    for j in range(16):
        for i in range(31):
            Swap | (x[128 + i], x[129 + i])
    for j in range(20):
        for i in range(31):
            Swap | (x[160 + i], x[161 + i])
    for j in range(24):
        for i in range(31):
            Swap | (x[192 + i], x[193 + i])
    for j in range(28):
        for i in range(31):
            Swap | (x[224 + i], x[225 + i])

def Constant_Multiplication(eng, x, result, c):

    if(c==1):
        CNOT | (x[0], result[0])
        CNOT | (x[1], result[1])
        CNOT | (x[2], result[2])
        CNOT | (x[3], result[3])

    if(c==2):
        CNOT | (x[0], result[1])
        CNOT | (x[1], result[2])
        CNOT | (x[2], result[3])
        CNOT | (x[3], result[0])
        CNOT | (x[3], result[1])

    if (c == 3):
        CNOT | (x[0], result[0])
        CNOT | (x[3], result[0])
        CNOT | (x[0], result[1])
        CNOT | (x[3], result[1])
        CNOT | (x[1], result[1])
        CNOT | (x[2], result[2])
        CNOT | (x[1], result[2])
        CNOT | (x[3], result[3])
        CNOT | (x[2], result[3])

    if(c==4):
        CNOT | (x[2], result[0])
        CNOT | (x[2], result[1])
        CNOT | (x[3], result[1])
        CNOT | (x[0], result[2])
        CNOT | (x[3], result[2])
        CNOT | (x[1], result[3])

    if(c==5):
        CNOT | (x[0], result[0])
        CNOT | (x[2], result[0])

        CNOT | (x[0], result[2])
        CNOT | (x[2], result[2])
        CNOT | (x[1], result[3])
        CNOT | (x[3], result[3])

        CNOT | (x[3], result[1])
        CNOT | (x[2], result[1])
        CNOT | (x[1], result[1])
        CNOT | (x[3], result[2])

    if(c==6):
        CNOT | (x[3], result[0])
        CNOT | (x[2], result[0])
        CNOT | (x[0], result[1])
        CNOT | (x[2], result[1])
        CNOT | (x[0], result[2])
        CNOT | (x[1], result[2])
        CNOT | (x[3], result[2])
        CNOT | (x[1], result[3])
        CNOT | (x[2], result[3])

    if(c==7):
        CNOT | (x[0], result[2])
        CNOT | (x[1], result[2])
        CNOT | (x[2], result[2])
        CNOT | (x[3], result[2])

        CNOT | (x[0], result[0])
        CNOT | (x[2], result[0])
        CNOT | (x[3], result[0])

        CNOT | (x[0], result[1])
        CNOT | (x[1], result[1])
        CNOT | (x[2], result[1])

        CNOT | (x[1], result[3])
        CNOT | (x[2], result[3])
        CNOT | (x[3], result[3])

    if(c==8):

        CNOT | (x[1], result[0])
        CNOT | (x[1], result[1])
        CNOT | (x[2], result[1])
        CNOT | (x[2], result[2])
        CNOT | (x[3], result[2])
        CNOT | (x[3], result[3])
        CNOT | (x[0], result[3])

    if(c==9):
        CNOT | (x[0], result[0])
        CNOT | (x[1], result[0])
        CNOT | (x[2], result[1])
        CNOT | (x[3], result[2])
        CNOT | (x[0], result[3])

    if(c==10):
        CNOT | (x[0], result[1])
        CNOT | (x[1], result[1])
        CNOT | (x[2], result[1])
        CNOT | (x[3], result[1])
        CNOT | (x[1], result[2])
        CNOT | (x[2], result[2])
        CNOT | (x[3], result[2])
        CNOT | (x[0], result[3])
        CNOT | (x[2], result[3])
        CNOT | (x[3], result[3])
        CNOT | (x[3], result[0])
        CNOT | (x[1], result[0])

    if (c == 11):
        CNOT | (x[0], result[3])
        CNOT | (x[2], result[3])
        CNOT | (x[0], result[1])
        CNOT | (x[2], result[1])
        CNOT | (x[3], result[1])

        CNOT | (x[1], result[2])
        CNOT | (x[3], result[2])

        CNOT | (x[1], result[0])
        CNOT | (x[3], result[0])
        CNOT | (x[0], result[0])

    if (c == 12):
        CNOT | (x[1], result[1])
        CNOT | (x[3], result[1])
        CNOT | (x[1], result[3])
        CNOT | (x[3], result[3])
        CNOT | (x[0], result[3])
        CNOT | (x[1], result[0])
        CNOT | (x[2], result[0])
        CNOT | (x[2], result[2])
        CNOT | (x[0], result[2])

    if (c == 13):
        CNOT | (x[0], result[3])
        CNOT | (x[1], result[3])
        CNOT | (x[0], result[0])
        CNOT | (x[1], result[0])
        CNOT | (x[2], result[0])
        CNOT | (x[0], result[2])
        CNOT | (x[3], result[1])

    if(c==14):
        CNOT | (x[0], result[3])
        CNOT | (x[1], result[3])
        CNOT | (x[2], result[3])
        CNOT | (x[3], result[3])

        CNOT | (x[1], result[0])
        CNOT | (x[2], result[0])
        CNOT | (x[3], result[0])

        CNOT | (x[0], result[2])
        CNOT | (x[1], result[2])
        CNOT | (x[2], result[2])
        CNOT | (x[0], result[1])
        CNOT | (x[1], result[1])

    if (c == 15):
        CNOT | (x[0], result[3])
        CNOT | (x[1], result[3])
        CNOT | (x[2], result[3])
        CNOT | (x[0], result[0])
        CNOT | (x[1], result[0])
        CNOT | (x[2], result[0])
        CNOT | (x[3], result[0])
        CNOT | (x[0], result[1])
        CNOT | (x[0], result[2])
        CNOT | (x[1], result[2])

def print_state(eng, x):

    All(Measure) | x
    print('\nState\n')
    for i in range(32):
        for j in range(4):
            print(int(x[4*(i+1)-1-j]), end='')
        print(" ", end='')
        if((i+1) % 8 == 0):
            print('\n')

def Message_XOR(eng, k, rc, bit):
    for i in range(bit):
        if(rc >> i & 1):
             X | k[i]

def Message_XOR2(eng, k, rc, bit):
    for i in range(bit):
        if(rc >> (i+128) & 1):
             X | k[i]

def Swap_result(eng, x, result):
    for i in range(256):
        Swap | (result[i], x[i])


Resource = ResourceCounter()
eng = MainEngine(Resource)
Photon(eng, 0x201f1e1d1c1b1a191817161514131211100f0e0d0c0b0a09080706050403020100, 256)
print('\n')
print(Resource)
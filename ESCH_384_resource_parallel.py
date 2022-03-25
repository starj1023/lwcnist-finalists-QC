
from projectq.ops import H, CNOT, Measure, Toffoli, X, All , Swap
from projectq import MainEngine
from projectq.backends import ResourceCounter, ClassicalSimulator
from projectq.meta import Loop, Compute, Uncompute, Control


def ESCH(eng, M_value, M_len):

    M = eng.allocate_qureg(M_len)
    #Round_constant_XOR(eng, M, M_value, M_len)
    S = eng.allocate_qureg(512)
    carry = eng.allocate_qureg(8)

    if (M_len != 0):
        if(M_len % 128 == 0):
            l = int(M_len / 128)
        else :
            l = int(M_len / 128) + 1
    else:
        l = 1

    for i in range(l-1):
        M4(eng, M[128*i: 128*i+128], S)
        Sparkle(eng, S, carry, 8)

    # Last block
    l_len = int(M_len - 128 * (l - 1))
    if (l_len != 128):
        padding = eng.allocate_qureg(128 - l_len)
        X | padding[7]

    M_last = []
    for i in range(l_len):
        M_last.append(M[128 * (l - 1) + i])
    if (l_len != 128):
        for i in range(128 - l_len):
            M_last.append(padding[i])

    M4(eng, M_last, S)

    if (l_len ==128):
        X | S[281]
    else:
        X | S[280]

    Sparkle(eng, S, carry, 12)

    result1 = eng.allocate_qureg(128)

    for i in range(128):
        CNOT | (S[511 - i], result1[127 - i])

    Sparkle(eng, S, carry, 8)

    result2 = eng.allocate_qureg(128)

    for i in range(128):
        CNOT | (S[511 - i], result2[127 - i])

    Sparkle(eng, S, carry, 8)

def M4(eng, M, S):

    x0 = M[0:32]
    y0 = M[32:64]
    x1 = M[64:96]
    y1 = M[96:128]

    XOR_32(eng, x0, S[480:512])
    XOR_32(eng, y0, S[448:480])
    XOR_32(eng, x1, S[416:448])
    XOR_32(eng, y1, S[384:416])

    XOR_32(eng, y0, y1)
    XOR_16(eng, y1[0:16], y1[16:32]) # a+b || b
    #for i in range(16):
    #    Swap | (y1[i], y1[16+i])     # b || a+ b

    XOR_32(eng, y1, S[480:512])
    XOR_32(eng, y1, S[416:448])
    XOR_32(eng, y1, S[352:384])
    XOR_32(eng, y1, S[288:320])

    XOR_32(eng, x0, x1)
    XOR_16(eng, x1[0:16], x1[16:32])  # a+b || b
    #for i in range(16):
    #    Swap | (x1[i], x1[16 + i])

    XOR_32(eng, x1, S[448:480])
    XOR_32(eng, x1, S[384:416])
    XOR_32(eng, x1, S[320:352])
    XOR_32(eng, x1, S[256:288])

def Sparkle(eng, x, carry, number):

    c = (0xB7E15162, 0xBF715880, 0x38B4DA56, 0x324E7738, 0xBB1185EB, 0x4F7C7B57, 0xCFBFA1C8, 0xC2B3293D)

    x7 = []
    y7 = []
    x6 = []
    y6 = []
    y5 = []
    x5 = []
    y4 = []
    x4 = []
    y3 = []
    x3 = []
    y2 = []
    x2 = []
    y1 = []
    x1 = []
    y0 = []
    x0 = []

    for i in range(8):
        y7.append(x[i])
        x7.append(x[i + 32])
        y6.append(x[i + 64])
        x6.append(x[i + 96])
        y5.append(x[i + 128])
        x5.append(x[i + 160])
        y4.append(x[i + 192])
        x4.append(x[i + 224])
        y3.append(x[i + 256])
        x3.append(x[i + 288])
        y2.append(x[i + 320])
        x2.append(x[i + 352])
        y1.append(x[i + 384])
        x1.append(x[i + 416])
        y0.append(x[i + 448])
        x0.append(x[i + 480])
    for i in range(8):
        y7.append(x[8 + i])
        x7.append(x[8 + i + 32])
        y6.append(x[8 + i + 64])
        x6.append(x[8 + i + 96])
        y5.append(x[8 + i + 128])
        x5.append(x[8 + i + 160])
        y4.append(x[8 + i + 192])
        x4.append(x[8 + i + 224])
        y3.append(x[8 + i + 256])
        x3.append(x[8 + i + 288])
        y2.append(x[8 + i + 320])
        x2.append(x[8 + i + 352])
        y1.append(x[8 + i + 384])
        x1.append(x[8 + i + 416])
        y0.append(x[8 + i + 448])
        x0.append(x[8 + i + 480])
    for i in range(8):
        y7.append(x[16 + i])
        x7.append(x[16 + i + 32])
        y6.append(x[16 + i + 64])
        x6.append(x[16 + i + 96])
        y5.append(x[16 + i + 128])
        x5.append(x[16 + i + 160])
        y4.append(x[16 + i + 192])
        x4.append(x[16 + i + 224])
        y3.append(x[16 + i + 256])
        x3.append(x[16 + i + 288])
        y2.append(x[16 + i + 320])
        x2.append(x[16 + i + 352])
        y1.append(x[16 + i + 384])
        x1.append(x[16 + i + 416])
        y0.append(x[16 + i + 448])
        x0.append(x[16 + i + 480])
    for i in range(8):
        y7.append(x[24 + i])
        x7.append(x[24 + i + 32])
        y6.append(x[24 + i + 64])
        x6.append(x[24 + i + 96])
        y5.append(x[24 + i + 128])
        x5.append(x[24 + i + 160])
        y4.append(x[24 + i + 192])
        x4.append(x[24 + i + 224])
        y3.append(x[24 + i + 256])
        x3.append(x[24 + i + 288])
        y2.append(x[24 + i + 320])
        x2.append(x[24 + i + 352])
        y1.append(x[24 + i + 384])
        x1.append(x[24 + i + 416])
        y0.append(x[24 + i + 448])
        x0.append(x[24 + i + 480])

    for i in range(number):

        Constant_XOR(eng, y0, c[i%8])
        Constant_XOR(eng, y1, i)

        AC(eng, x0, y0, carry[0], c[0])
        AC(eng, x1, y1, carry[1], c[1])
        AC(eng, x2, y2, carry[2], c[2])
        AC(eng, x3, y3, carry[3], c[3])
        AC(eng, x4, y4, carry[4], c[4])
        AC(eng, x5, y5, carry[5], c[5])
        AC(eng, x6, y6, carry[6], c[6])
        AC(eng, x7, y7, carry[7], c[7])

        L8(eng, x0, x1, x2, x3, x4, x5, x6, x7, y0, y1, y2, y3, y4, y5, y6, y7)



def Constant_XOR(eng, k, rc):
    for i in range(32):
        if(rc >> i & 1):
             X | k[i]

def CDKM(eng, a, b, c, n):
    for i in range(n - 2):
        CNOT | (a[i + 1], b[i + 1])

    CNOT | (a[1], c)
    Toffoli | (a[0], b[0], c)
    CNOT | (a[2], a[1])
    Toffoli | (c, b[1], a[1])
    CNOT | (a[3], a[2])

    for i in range(n - 5):
        Toffoli | (a[i + 1], b[i + 2], a[i + 2])
        CNOT | (a[i + 4], a[i + 3])

    Toffoli | (a[n - 4], b[n - 3], a[n - 3])
    CNOT | (a[n - 2], b[n - 1])
    CNOT | (a[n - 1], b[n - 1])
    Toffoli | (a[n - 3], b[n - 2], b[n - 1])

    for i in range(n - 3):
        X | b[i + 1]

    CNOT | (c, b[1])

    for i in range(n - 3):
        CNOT | (a[i + 1], b[i + 2])

    Toffoli | (a[n - 4], b[n - 3], a[n - 3])

    for i in range(n - 5):
        Toffoli | (a[n - 5 - i], b[n - 4 - i], a[n - 4 - i])
        CNOT | (a[n - 2 - i], a[n - 3 - i])
        X | (b[n - 3 - i])

    Toffoli | (c, b[1], a[1])
    CNOT | (a[3], a[2])
    X | b[2]
    Toffoli | (a[0], b[0], c)
    CNOT | (a[2], a[1])
    X | b[1]
    CNOT | (a[1], c)

    for i in range(n-1):
        CNOT | (a[i], b[i])

def AC(eng, x, y, carry, i):

    y = logical_Swap(eng, y, 31)
    CDKM(eng, y, x, carry, 32)
    y = logical_Swap(eng, y, 1) #reverse
    XOR_32_rotation(eng, x, y, 24)
    Constant_XOR(eng, x, i)

    y = logical_Swap(eng, y, 17)
    CDKM(eng, y, x, carry, 32)
    y = logical_Swap(eng, y, 15)  # reverse
    XOR_32_rotation(eng, x, y, 17)
    Constant_XOR(eng, x, i)

    CDKM(eng, y, x, carry, 32)
    XOR_32_rotation(eng, x, y, 31)
    Constant_XOR(eng, x, i)

    y = logical_Swap(eng, y, 24)
    CDKM(eng, y, x, carry, 32)
    y = logical_Swap(eng, y, 8)  # reverse
    XOR_32_rotation(eng, x, y, 16)
    Constant_XOR(eng, x, i)

def logical_Swap(eng, x, n):

    new_x = []
    for i in range(32):
        new_x.append(x[(n+i)%32])
    return new_x

def XOR_32_rotation(eng, a, b, a_first):
    for i in range(32):
        CNOT | (a[(a_first+i) % 32], b[i])

def XOR_32(eng, a, b):
    for i in range(32):
        CNOT | (a[i], b[i])

def XOR_16(eng, a, b):
    for i in range(16):
        CNOT | (a[i], b[i])

def Swap_32(eng, a, b):
    for i in range(32):
        Swap | (a[i], b[i])

def L8(eng, x0, x1, x2, x3, x4, x5, x6, x7, y0, y1, y2, y3, y4, y5, y6, y7):

    with Compute(eng):
        XOR_32(eng, y0, y3)
        XOR_32(eng, y1, y3)
        XOR_32(eng, y2, y3)
        XOR_16(eng, y3[0:16], y3[16:32]) # a+b || b

    XOR_16(eng, y3[16:32], x5[0:16])
    XOR_16(eng, y3[0:16], x5[16:32])
    XOR_32(eng, x1, x5)

    XOR_16(eng, y3[16:32], x6[0:16])
    XOR_16(eng, y3[0:16], x6[16:32])
    XOR_32(eng, x2, x6)

    XOR_16(eng, y3[16:32], x7[0:16])
    XOR_16(eng, y3[0:16], x7[16:32])
    XOR_32(eng, x3, x7)

    XOR_16(eng, y3[16:32], x4[0:16])
    XOR_16(eng, y3[0:16], x4[16:32])
    XOR_32(eng, x0, x4)

    Uncompute(eng)

    with Compute(eng):
        XOR_32(eng, x0, x3)
        XOR_32(eng, x1, x3)
        XOR_32(eng, x2, x3)
        XOR_16(eng, x3[0:16], x3[16:32])  # a+b || b

    XOR_16(eng, x3[16:32], y5[0:16])
    XOR_16(eng, x3[0:16], y5[16:32])
    XOR_32(eng, y1, y5)

    XOR_16(eng, x3[16:32], y6[0:16])
    XOR_16(eng, x3[0:16], y6[16:32])
    XOR_32(eng, y2, y6)

    XOR_16(eng, x3[16:32], y7[0:16])
    XOR_16(eng, x3[0:16], y7[16:32])
    XOR_32(eng, y3, y7)

    XOR_16(eng, x3[16:32], y4[0:16])
    XOR_16(eng, x3[0:16], y4[16:32])
    XOR_32(eng, y0, y4)

    Uncompute(eng)

    #Swap_32(eng, x0, x4)
    #Swap_32(eng, x1, x5)
    #Swap_32(eng, x2, x6)
    #Swap_32(eng, x3, x7)

    #Swap_32(eng, y0, y4)
    #Swap_32(eng, y1, y5)
    #Swap_32(eng, y2, y6)
    #Swap_32(eng, y3, y7)

    #Swap_32(eng, x0, x1)
    #Swap_32(eng, y0, y1)
    #Swap_32(eng, x1, x2)
    #Swap_32(eng, y1, y2)
    #Swap_32(eng, x2, x3)
    #Swap_32(eng, y2, y3)


def Round_constant_XOR(eng, k, rc, bit):
    for i in range(bit):
        if(rc >> i & 1):
             X | k[i]

#print('\n')
Resource = ResourceCounter()
eng = MainEngine(Resource)
(ESCH(eng, 0x0f0e0d0c0b0a09080706050403020100201f1e1d1c1b1a191817161514131211100f0e0d0c0b0a09080706050403020100, 384))
print('\n')
print(Resource)

eng.flush()

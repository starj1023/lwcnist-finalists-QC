import math
from projectq import MainEngine
from projectq.ops import H, CNOT, Measure, Toffoli, X, All, Swap
from projectq.backends import CircuitDrawer, ResourceCounter, CommandPrinter, ClassicalSimulator
from projectq.meta import Loop, Compute, Uncompute, Control
import random

def S_and_constant_xor(eng, constant, qubit):
    for i in range(64): #length
        if(constant & 1 == 1 ):
            X | qubit[i]
        constant = constant >> 1

def Message_XOR(eng, constant, qubit, len):
    for i in range(len): #length
        if(constant & 1 == 1 ):
            X | qubit[i]
        constant = constant >> 1


def Addition_Constanct(eng, i ,x2):
    Constant = (0xf0, 0xe1, 0xd2, 0xc3, 0xb4, 0xa5, 0x96, 0x87, 0x78, 0x69, 0x5a, 0x4b)
    S_and_constant_xor(eng, Constant[i], x2)


def Reverse(eng,x0,x1,x2,x3,x4):
    # x1
    for i in range(64):
        Toffoli | (x2[i], x3[i], x1[i])

    for i in range(64):
        X | x2[i]
        X | x1[i]

    # x0
    for i in range(64):
        CNOT | (x4[i], x0[i])
        CNOT | (x0[i], x1[i])
        Toffoli | (x1[i], x2[i], x0[i])
        X | x1[i]
        X | x0[i]

    #x4
    for i in range(64):
        Toffoli | (x0[i], x1[i], x4[i])
        X | x0[i]


def Substitution_LinearDiffusion_Layer(eng, x0,x1, x2, x3, x4, pa, pb):
    for i in range(pa+pb):
        x_0 = eng.allocate_qureg(64)
        x_1 = eng.allocate_qureg(64)
        x_2 = eng.allocate_qureg(64)
        x_3 = eng.allocate_qureg(64)
        x_4 = eng.allocate_qureg(64)

        Addition_Constanct(eng, i, x2)

        for i in range(64):
            CNOT | (x4[i], x0[i])
            CNOT | (x1[i], x2[i])
            CNOT | (x3[i], x4[i])

        #x4
        for i in range(64):
            X | x0[i]
            Toffoli | (x0[i], x1[i], x4[i])


        for i in range(64):
            CNOT | (x4[i], x_4[i])

        for i in range(64):
            CNOT | (x4[(i+7)%64], x_4[i])
        for i in range(64):
            CNOT | (x4[(i+41)%64], x_4[i])

        #x0
        for i in range(64):
            X | x0[i]
            X | x1[i]
            Toffoli | (x1[i], x2[i], x0[i])
            CNOT | (x0[i], x1[i])
            CNOT | (x4[i], x0[i])

        for i in range(64):
            CNOT | (x0[i], x_0[i])
        for i in range(64):
            CNOT | (x0[(19+i)%64], x_0[i])
        for i in range(64):
            CNOT | (x0[(28+i)%64], x_0[i])

        #x1
        for i in range(64):
            X | x1[i]
            X | x2[i]

        for i in range(64):
            Toffoli | (x2[i], x3[i], x1[i])
        for i in range(64):
            CNOT | (x1[i], x_1[i])

        for i in range(64):
            CNOT | (x1[(61+i)%64], x_1[i])
        for i in range(64):
            CNOT | (x1[(39+i)%64], x_1[i])

        Reverse(eng, x0, x1, x2, x3, x4)

        #x2
        for i in range(64):
            X | x3[i]
        for i in range(64):
            Toffoli | (x3[i], x4[i], x2[i])
        for i in range(64):
            CNOT | (x2[i], x3[i])
        for i in range(64):
            X | x2[i]
        for i in range(64):
            CNOT | (x2[i], x_2[i])


        for i in range(64):
            CNOT | (x2[(1+i)%64], x_2[i])
        for i in range(64):
            CNOT | (x2[(6+i)%64], x_2[i])

        #x3
        for i in range(64):
            X | x3[i]
            X | x4[i]
        for i in range(64):
            Toffoli | (x4[i], x0[i], x3[i])
        for i in range(64):
            CNOT | (x3[i], x_3[i])

        for i in range(64):
            X | x4[i]

        for i in range(64):
            CNOT | (x3[(10+i)%64], x_3[i])
        for i in range(64):
            CNOT | (x3[(17+i)%64], x_3[i])


        for i in range(64):
            Swap | (x0[i], x_0[i])
            Swap | (x1[i], x_1[i])
            Swap | (x2[i], x_2[i])
            Swap | (x3[i], x_3[i])
            Swap | (x4[i], x_4[i])

def main(eng, M_value, len):

    M = eng.allocate_qureg(len)
    Message_XOR(eng, M_value, M, len)

    temp = len+1
    if (temp % 64 == 0):
        l = int(temp / 64)
    else:
        l = int(temp / 64) + 1

    pa = 12
    pb = 12
    S = (0xee9398aadb67f03d, 0x8bb21831c60f1002, 0xb48a92db98d5da62, 0x43189921b8f8e3e8, 0x348fa5c9d525e140)


    # S => x0 | x1 | x2 | x3 | x4
    # x0 => S_r , x1 | x2 | x3 | X4 => S_c
    x0 = eng.allocate_qureg(64)
    x1 = eng.allocate_qureg(64)
    x2 = eng.allocate_qureg(64)
    x3 = eng.allocate_qureg(64)
    x4 = eng.allocate_qureg(64)

    S_and_constant_xor(eng, S[0], x0)
    S_and_constant_xor(eng, S[1], x1)
    S_and_constant_xor(eng, S[2], x2)
    S_and_constant_xor(eng, S[3], x3)
    S_and_constant_xor(eng, S[4], x4)

    # Absorbing
    for number in range(l):
        if(number != l-1):
            for i in range(64):
                CNOT | (M[len - (64*(number+1)) + i], x0[i])

            Substitution_LinearDiffusion_Layer(eng, x0, x1, x2, x3, x4, 0, pb)

        else :
            left_len = len-64*number
            start = 64-left_len
            for i in range(left_len):
                CNOT | (M[i], x0[i+start])

    #Squeezing
    Substitution_LinearDiffusion_Layer(eng, x0, x1, x2, x3, x4, pa, 0)

    print("HASH")
    for i in range(4):
        All(Measure) | x0
        for i in range(64):
            print(int(x0[63 - i]), end='')
        print('\n')

        Substitution_LinearDiffusion_Layer(eng, x0, x1, x2, x3, x4, 0, pb)

sim = ClassicalSimulator()
eng = MainEngine(sim)
main(eng, 0x201f1e1d1c1b1a191817161514131211100f0e0d0c0b0a09080706050403020100, 256)
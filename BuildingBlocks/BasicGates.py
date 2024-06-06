import os
import sys

# directory reach
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from utilities import printErrorAndExit

def NOT(val1):
    """
    @param val1 (int): The value to be negated (can be more than single bit)
    @return (int): The negated value
    """
    return (2**len(bin(val1)[2:])-1) & ~val1

def AND(val1, val2):
    """
    @param val1 (int): The first value to be ANDed
    @param val2 (int): The second value to be ANDed
    @return (int): The result of the AND operation
    """
    return val1 & val2

def OR(val1, val2):
    """
    @param val1 (int): The first value to be ORed
    @param val2 (int): The second value to be ORed
    @return (int): The result of the OR operation
    """
    return val1 | val2

def XOR(val1, val2):
    """
    @param val1 (int): The first value to be XORed
    @param val2 (int): The second value to be XORed
    @return (int): The result of the XOR operation
    """
    return val1 ^ val2

def NAND(val1, val2):
    """
    @param val1 (int): The first value to be NANDed
    @param val2 (int): The second value to be NANDed
    @return (int): The result of the NAND operation
    """
    return NOT(AND(val1, val2))

def NOR(val1, val2):
    """
    @param val1 (int): The first value to be NORed
    @param val2 (int): The second value to be NORed
    @return (int): The result of the NOR operation
    """
    return NOT(OR(val1, val2))

def XNOR(val1, val2):
    """
    @param val1 (int): The first value to be XNORed
    @param val2 (int): The second value to be XNORed
    @return (int): The result of the XNOR operation
    """
    return NOT(XOR(val1, val2))

def MUX(sel, val1, val2):
    """
    @param sel (int): The selection bit (0 or 1)
    @param val1 (int): The first value to be selected (0 or 1)
    @param val2 (int): The second value to be selected (0 or 1)
    @return (int): The selected value (0 or 1)
    """
    if (sel > 1 and val1 > 1 and val2 > 1):
        printErrorAndExit("selection, val1, val2 can only be 0 or 1")

    return OR(AND(sel, val1), AND(NOT(sel), val2))

def DMUX(sel, val):
    """
    @param sel (int): The selection bit (0 or 1)
    @param val (int): The value to be demultiplexed (0 or 1)
    @return (int, int): The demultiplexed values (2 bits)
    """
    if (sel > 1 and val):
        printErrorAndExit("selection, val can only be 0 or 1")

    return (MUX(sel, val, 0) << 1) & MUX(NOT(sel), val, 0)
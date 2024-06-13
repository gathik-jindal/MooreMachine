import os
import sys

# directory reach
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from utilities import checkType, bitCount
from pydig import pydig as pd
from usableBlocks import Combinational as Comb
import random


class NOT(Comb):
    """
    This class represents the NOT gate.
    All the incoming lines will be negated.
    """

    def __init__(self, pydig: pd, delay: float, initialValue: int, plot: bool, blockID: str):
        """
        @param pydig : pydig object
        @param delay : the time delay for the NOT gate
        @param initialValue : The initial output value given by this block at t = 0 while running
        @param plot : boolean value whether to plot this moore machine or not
        @param blockID : the id of this machine. If None, then new unique ID is given.
        """
        checkType([(pydig, pd), (delay, (float, int)), (initialValue, int), (plot, bool), (blockID, str)])
        super().__init__(func=self.__func, env=pydig.getEnv(), blockID=blockID, maxOutSize=1, delay=delay, plot=plot, initialValue=initialValue)

        pydig.combinationalFromObject(self)  # make this object a part of the pydig object

    def __func(self, val):
        """
        @param val (int): The value to be negated (can be more than single bit)
        @return (int): The negated value
        """
        return (2**bitCount(val)-1) & ~val


class AND(Comb):
    """
    This class represents the AND gate.
    Half the incoming lines will be ANDed with the other half.

    Lets say the incoming bits are: 10101100
    Then the first 4 bits will be ANDed with the last 4 bits, in this order: 1010 & 1100
    """

    def __init__(self, pydig: pd, delay: float, initialValue: int, plot: bool, blockID: str):
        """
        @param pydig : pydig object
        @param delay : the time delay for the and gate
        @param initialValue : The initial output value given by this block at t = 0 while running
        @param plot : boolean value whether to plot this block or not
        @param blockID : the id of this block. If None, then new unique ID is given.
        """
        checkType([(pydig, pd), (delay, (float, int)), (initialValue, int), (plot, bool), (blockID, str)])
        super().__init__(func=self.__func, env=pydig.getEnv(), blockID=blockID, maxOutSize=1, delay=delay, plot=plot, initialValue=initialValue)

        pydig.combinationalFromObject(self)  # make this object a part of the pydig object

    def __func(self, val):
        """
        @param val (int): The value that's going to be used to AND
        @return (int): The result of the AND operation
        """
        ans = 1
        while val:
            ans = ans & (val%2)
            val = val >> 1
        return ans


class OR(Comb):
    """
    This class represents the OR gate.
    Half the incoming lines will be ORed with the other half.

    Lets say the incoming bits are: 10101100
    Then the first 4 bits will be ORed with the last 4 bits, in this order: 1010 & 1100
    """

    def __init__(self, pydig: pd, delay: float, initialValue: int, plot: bool, blockID: str):
        """
        @param pydig : pydig object
        @param delay : the time delay for the OR gate
        @param initialValue : The initial output value given by this block at t = 0 while running
        @param plot : boolean value whether to plot this block or not
        @param blockID : the id of this block. If None, then new unique ID is given.
        """
        checkType([(pydig, pd), (delay, (float, int)), (initialValue, int), (plot, bool), (blockID, str)])
        super().__init__(func=self.__func, env=pydig.getEnv(), blockID=blockID, maxOutSize=1, delay=delay, plot=plot, initialValue=initialValue)

        pydig.combinationalFromObject(self)  # make this object a part of the pydig object

    def __func(self, val):
        """
        @param val (int): The value to be ORed
        @return (int): The result of the OR operation
        """
        numBits = bitCount(val)
        val1 = val >> (numBits // 2)
        val2 = val & ((1 << (numBits // 2)) - 1)
        return val1 | val2


class XOR(Comb):
    """
    This class represents the XOR gate.
    Half the incoming lines will be XORed with the other half.

    Lets say the incoming bits are: 10101100
    Then the first 4 bits will be XORed with the last 4 bits, in this order: 1010 & 1100
    """

    def __init__(self, pydig: pd, delay: float, initialValue: int, plot: bool, blockID: str):
        """
        @param pydig : pydig object
        @param delay : the time delay for the XOR gate
        @param initialValue : The initial output value given by this block at t = 0 while running
        @param plot : boolean value whether to plot this block or not
        @param blockID : the id of this block. If None, then new unique ID is given.
        """
        checkType([(pydig, pd), (delay, (float, int)), (initialValue, int), (plot, bool), (blockID, str)])
        super().__init__(func=self.__func, env=pydig.getEnv(), blockID=blockID, maxOutSize=1, delay=delay, plot=plot, initialValue=initialValue)

        pydig.combinationalFromObject(self)  # make this object a part of the pydig object

    def __func(self, val):
        """
        @param val (int): The value to be XORed
        @return (int): The result of the XOR operation
        """
        numBits = bitCount(val)
        val1 = val >> (numBits // 2)
        val2 = val & ((1 << (numBits // 2)) - 1)
        return val1 ^ val2


class NAND(Comb):
    """
    This class represents the NAND gate.
    Half the incoming lines will be NANDed with the other half.

    Lets say the incoming bits are: 10101100
    Then the first 4 bits will be NANDed with the last 4 bits, in this order: 1010 & 1100
    """

    def __init__(self, pydig: pd, delay: float, initialValue: int, plot: bool, blockID: str):
        """
        @param pydig : pydig object
        @param delay : the time delay for the NAND gate
        @param initialValue : The initial output value given by this block at t = 0 while running
        @param plot : boolean value whether to plot this block or not
        @param blockID : the id of this block. If None, then new unique ID is given.
        """
        self.__andGate = AND(pydig, delay, initialValue, False, blockID + str(random.randint(10, 10000)))
        self.__notGate = NOT(pydig, 0, initialValue, plot, blockID)

        self.__andGate.output() > self.__notGate.input()

    def input(self, left=None, right=None):
        """
        @return obj : instance of the andGate object
        """
        return self.__andGate.input(left, right)

    def output(self, left=0, right=None):
        """
        @return obj : instance of the notGate object
        """
        return self.__notGate.output(left, right)
    
    def getScopeDump(self):
        """
        @return dict : the scope dump values for this block.
        """
        return self.__notGate.getScopeDump()


class NOR(Comb):
    """
    This class represents the NOR gate.
    Half the incoming lines will be NORed with the other half.

    Lets say the incoming bits are: 10101100
    Then the first 4 bits will be NORed with the last 4 bits, in this order: 1010 & 1100
    """

    def __init__(self, pydig: pd, delay: float, initialValue: int, plot: bool, blockID: str):
        """
        @param pydig : pydig object
        @param delay : the time delay for the NOR gate
        @param initialValue : The initial output value given by this block at t = 0 while running
        @param plot : boolean value whether to plot this block or not
        @param blockID : the id of this block. If None, then new unique ID is given.
        """
        self.__orGate = OR(pydig, delay, initialValue, False, blockID + str(random.randint(10, 10000)))
        self.__notGate = NOT(pydig, 0, initialValue, plot, blockID)

        self.__orGate.output() > self.__notGate.input()
    
    def input(self, left=None, right=None):
        """
        @return obj : instance of the orGate object
        """
        return self.__orGate.input(left, right)

    def output(self, left=0, right=None):
        """
        @return obj : instance of the notGate object
        """
        return self.__notGate.output(left, right)
    
    def getScopeDump(self):
        """
        @return dict : the scope dump values for this block.
        """
        return self.__notGate.getScopeDump()


class XNOR(Comb):
    """
    This class represents the XNOR gate.
    Half the incoming lines will be XNORed with the other half.

    Lets say the incoming bits are: 10101100
    Then the first 4 bits will be XNORed with the last 4 bits, in this order: 1010 & 1100
    """

    def __init__(self, pydig: pd, delay: float, initialValue: int, plot: bool, blockID: str):
        """
        @param pydig : pydig object
        @param delay : the time delay for the XNOR gate
        @param initialValue : The initial output value given by this block at t = 0 while running
        @param plot : boolean value whether to plot this block or not
        @param blockID : the id of this block. If None, then new unique ID is given.
        """
        self.__xorGate = XOR(pydig, delay, initialValue, False, blockID + str(random.randint(10, 10000)))
        self.__notGate = NOT(pydig, 0, initialValue, plot, blockID)

        self.__xorGate.output() > self.__notGate.input()
    
    def input(self, left=None, right=None):
        """
        @return obj : instance of the xorGate object
        """
        return self.__xorGate.input(left, right)

    def output(self, left=0, right=None):
        """
        @return obj : instance of the notGate object
        """
        return self.__notGate.output(left, right)
    
    def getScopeDump(self):
        """
        @return dict : the scope dump values for this block.
        """
        return self.__notGate.getScopeDump()


class MUX(Comb):
    """
    This class represents the MUX gate.
    If the selection bit is 0, then the first value is selected, else the second value is selected.

    The first bit is the selectin bit, and from rest of the bits, the first half is the first value and the second half is the second value.
    For example, if the input is 110101100, then the selection bit is 1, the first value is 1010 and the second value is 1100.
    """

    def __init__(self, pydig: pd, delay: float, initialValue: int, plot: bool, blockID: str):
        """
        @param pydig : pydig object
        @param delay : the time delay for the MUX gate
        @param initialValue : The initial output value given by this block at t = 0 while running
        @param plot : boolean value whether to plot this block or not
        @param blockID : the id of this block. If None, then new unique ID is given.
        """
        checkType([(pydig, pd), (delay, (float, int)), (initialValue, int), (plot, bool), (blockID, str)])
        super().__init__(func=self.__func, env=pydig.getEnv(), blockID=blockID, maxOutSize=1, delay=delay, plot=plot, initialValue=initialValue)

        pydig.combinationalFromObject(self)  # make this object a part of the pydig object

    def __func(self, val):
        """
        @param val (int): The value to be MUXed
        @return (int): The result of the MUX operation
        """
        length = bitCount(val)
        sel = val >> (length - 1) # getting selection bit
        val = val & ((1 << (length - 1)) - 1) # removing selection bit
        length -= 1
        val1 = val >> (length // 2) # getting first value
        val2 = val & ((1 << (length // 2)) - 1) # getting second value

        mask = 1 << ((length // 2) + 1) # obtaining the mask
        mask -= sel # subtracting sel from the mask, this decides which value to select
        
        return (val1 & n(mask)) | (val2 & mask)


# class DMUX(Comb):
#     """
#     This class represents the DMUX gate.
#     If the selection bit is 0, then the first value is selected, else the second value is selected.

#     The first bit is the selectin bit, and the rest of the bits are the values.
#     For example, if the input is 110, then the selection bit is 1, the first value is 1 and the second value is 0.
#     """

#     def __init__(self, pydig: pd, delay: float, initialValue: int, plot: bool, blockID: str):
#         """
#         @param pydig : pydig object
#         @param delay : the time delay for the DMUX gate
#         @param initialValue : The initial output value given by this block at t = 0 while running
#         @param plot : boolean value whether to plot this block or not
#         @param blockID : the id of this block. If None, then new unique ID is given.
#         """
#         checkType([(pydig, pd), (delay, (float, int)), (initialValue, int), (plot, bool), (blockID, str)])
#         super().__init__(func=self.__func, env=pydig.getEnv(), blockID=blockID, maxOutSize=2, delay=delay, plot=plot, initialValue=initialValue)

#         pydig.combinationalFromObject(self)  # make this object a part of the pydig object

#     def __func(self, val):
#         """
#         @param val (int): The value to be demultiplexed
#         @return (int, int): The demultiplexed values
#         """
#         sel = val >> 1
#         val = val & 1

#         return (val & n(sel), val & sel)
# def DMUX(sel, val):
#     """
#     @param sel (int): The selection bit (0 or 1)
#     @param val (int): The value to be demultiplexed (0 or 1)
#     @return (int, int): The demultiplexed values (2 bits)
#     """
#     if (sel > 1 and val):
#         printErrorAndExit("selection, val can only be 0 or 1")

#     return (MUX(sel, val, 0) << 1) & MUX(NOT(sel), val, 0)


def n(val):
    """
    @param val (int): The value to be negated
    @return (int): The negated value
    """
    
    mask = (1 << bitCount(val)) - 1
    return mask & ~val

if __name__ == "__main__":
    
    pysim = pd("Basic Gates")
    notGate = NOT(pysim, 0, 1, True, "Not Gate")
    andGate = AND(pysim, 0, 1, True, "And Gate")
    orGate = OR(pysim, 0, 1, True, "Or Gate")
    xorGate = XOR(pysim, 0, 1, True, "Xor Gate")
    nandGate = NAND(pysim, 0, 1, True, "Nand Gate")
    norGate = NOR(pysim, 0, 1, True, "Nor Gate")
    xnor = XNOR(pysim, 0, 1, True, "Xnor Gate")

    clock = pysim.clock(plot=True)

    clock.output() > notGate.input()
    clock.output() > andGate.input()
    clock.output() > orGate.input()
    clock.output() > xorGate.input()
    clock.output() > nandGate.input()
    clock.output() > norGate.input()
    clock.output() > xnor.input()

    pysim.run(10)

import os
import sys

# directory reach
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from utilities import checkType, bitCount
from pydig import pydig as pd
from blocks import HasOutputConnections

#### Aryan look at this

class SISO:
    """
    This class represents the SISO register.
    """

    def __init__(self, pydig: pd, size:int, clock, delay: float, initialValue: int, plot: bool, blockID: str):
        """
        @param pydig : pydig object
        @param delay : the time delay for each register in the SISO block.
        @param size : the number of registers in the SISO block
        @param initialValue : The initial output value given by each register in the block at t = 0 while running
        @param plot : boolean value whether to plot this block or not
        @param blockID : the id of this block. If None, then new unique ID is given.
        """
        checkType([(pydig, pd), (delay, (float, int)), (size, (int)), (initialValue, int), (plot, bool), (blockID, str)])
        self.__register = pydig.moore(maxOutSize=1, plot=plot, blockID=blockID, startingState=initialValue, clock = clock, register_delay = delay)
        self.__size = size
        self.__register.nsl = self.__nsl
        self.__register.ol = self.__ol

    def __nsl(self, ps,i):
        return ((ps*2)%(2**self.__size) + (i&1)) 

    def __ol(self, ps):
        return (ps>>(self.__size-1))&1
    
    def input(self, left=None, right=None):
        """
        @return obj : instance of the first register object
        """
        return self.__register.input(left,right)
    
    def output(self, left=0, right=None):
        """
        @return obj : instance of the last register object
        """
        return self.__register.output(left, right)

    def clock(self):
        """
        @return obj : instance of the clock object
        """
        return self.__register.clock()
    
    def __le__(self, other):
        self.__register.input() <= other
        return True

    def __gt__(self,other):
        self.__register.output() > other
        return True


class SIPO:
    """
    This class represents the SIPO register.
    """

    def __init__(self, pydig: pd, size:int, clock, delay: float, initialValue: int, plot: bool, blockID: str):
        """
        @param pydig : pydig object
        @param delay : the time delay for each register in the SISO block.
        @param size : the number of registers in the SISO block
        @param initialValue : The initial output value given by each register in the block at t = 0 while running
        @param plot : boolean value whether to plot this block or not
        @param blockID : the id of this block. If None, then new unique ID is given.
        """
        checkType([(pydig, pd), (delay, (float, int)), (size, (int)), (initialValue, int), (plot, bool), (blockID, str)])
        self.__register = pydig.moore(maxOutSize=size, plot=plot, blockID=blockID, startingState=initialValue, clock = clock, register_delay = delay)
        self.__size = size
        self.__register.nsl = self.__nsl
        self.__register.ol = self.__ol

    def __nsl(self, ps,i):
        return ((ps*2)%(2**self.__size) + (i&1)) 

    def __ol(self, ps):
        k = self.__size
        ans = 0
        while(k):
            k-=1
            ans = ans << 1
            ans += ps&1
            ps = ps >> 1
        return ans
    
    def input(self, left=None, right=None):
        """
        @return obj : instance of the first register object
        """
        return self.__register.input(left,right)
    
    def output(self, left=0, right=None):
        """
        @return obj : instance of the last register object
        """
        return self.__register.output(left, right)

    def clock(self):
        """
        @return obj : instance of the clock object
        """
        return self.__register.clock()
    
    def __le__(self, other):
        self.__register.input() <= other
        return True

    def __gt__(self,other):
        self.__register.output() > other
        return True


class PIPO:
    """
    This class represents the PIPO register.
    """

    def __init__(self, pydig: pd, size:int, clock, delay: float, initialValue: int, plot: bool, blockID: str):
        """
        @param pydig : pydig object
        @param delay : the time delay for each register in the SISO block.
        @param size : the number of registers in the SISO block
        @param initialValue : The initial output value given by each register in the block at t = 0 while running
        @param plot : boolean value whether to plot this block or not
        @param blockID : the id of this block. If None, then new unique ID is given.
        """
        checkType([(pydig, pd), (delay, (float, int)), (size, (int)), (initialValue, int), (plot, bool), (blockID, str)])
        self.__register = pydig.moore(maxOutSize=size, plot=plot, blockID=blockID, startingState=initialValue, clock = clock, register_delay = delay)
        self.__size = size
        self.__register.nsl = self.__nsl
        self.__register.ol = self.__ol

    def __nsl(self, ps, i):
        return i&(2**self.__size-1)

    def __ol(self, ps):
        return ps&(2**self.__size-1)
    
    def input(self, left=None, right=None):
        """
        @return obj : instance of the first register object
        """
        return self.__register.input(left,right)
    
    def output(self, left=0, right=None):
        """
        @return obj : instance of the last register object
        """
        return self.__register.output(left, right)

    def clock(self):
        """
        @return obj : instance of the clock object
        """
        return self.__register.clock()
    
    def __le__(self, other):
        self.__register.input() <= other
        return True

    def __gt__(self,other):
        self.__register.output() > other    
        return True

class PISO:
    """
    This class represents the PISO register.
    """

    def __init__(self, pydig: pd, size:int, clock, load, drive, delay: float, initialValue: int, plot: bool, blockID: str):
        """
        @param pydig : pydig object
        @param delay : the time delay for each register in the SISO block.
        @param size : the number of registers in the SISO block
        @param initialValue : The initial output value given by each register in the block at t = 0 while running
        @param plot : boolean value whether to plot this block or not
        @param blockID : the id of this block. If None, then new unique ID is given.
        """
        checkType([(pydig, pd), (delay, (float, int)), (size, (int)), (initialValue, int), (drive,int), (plot, bool), (blockID, str),(load,HasOutputConnections)])
        self.__register = pydig.moore(maxOutSize=size, plot=plot, blockID=blockID, startingState=initialValue, clock = clock, register_delay = delay)
        self.__drive = drive&1
        load.output() > self.__register.input()
        self.__size = size
        self.__register.nsl = self.__nsl
        self.__register.ol = self.__ol

    def __nsl(self, ps, i):
        if i&1:
            return (i>>1)&(2**self.__size-1)
        return ((ps*2)%(2**self.__size) + self.__drive) 

    def __ol(self, ps):
        return (ps>>(self.__size-1))&1
    
    def input(self, left=None, right=None):
        """
        @return obj : instance of the first register object
        """
        return self.__register.input(left,right)
    
    def output(self, left=0, right=None):
        """
        @return obj : instance of the last register object
        """
        return self.__register.output(left, right)

    def clock(self):
        """
        @return obj : instance of the clock object
        """
        return self.__register.clock()
    
    def __le__(self, other):
        self.__register.input() <= other
        return True

    def __gt__(self,other):
        self.__register.output() > other    
        return True


if __name__ == "__main__":
    
    pysim = pd("Basic Gates")

    clock = pysim.clock(plot=True, onTime=0.2, timePeriod=0.4, initialValue = 1)
    clock2 = pysim.clock(plot=True, onTime=2, timePeriod=4,initialValue = 1)
    o = pysim.output(plot = True)
    siso = SIPO(pysim, 4, clock, 0.1, 14, True, "SISO")
    clock2.output() > siso.input()
    siso.output() > o.input()

    pysim.run(20)

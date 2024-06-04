"""
This module contains the implementation of the SR Latch and D Latch.
The SR Latch is implemented using the NOR gate and the D Latch is
implemented using the SR Latch.
The SR Latch is a simple latch that has two inputs, S and R, and two
outputs, Q and ~Q.
The D Latch is a latch that has one input, D, and two outputs, Q and ~Q.

@author Abhirath, Aryan, Gathik
@date 4/12/2023
@version 1.6
"""

import os
import sys

# directory reach
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from blocks import Combinational as Comb, HasOutputConnections as HOC, Clock
from pydig import pydig as pd
from utilities import checkType


class SRLatch(Comb):
    __counter = 0

    def __init__(self, pydig: pd, SR: HOC, plot: bool = True):
        """
        @param pydig : pydig object
        @param SR : the set and reset signal
        @param plot : boolean value whether to plot this moore machine or not
        """
        checkType([(pydig, pd), (SR, HOC), (plot, bool)])

        SRLatch.__counter += 1

        super().__init__(func=lambda x: x, env=pydig.getEnv(), blockID=f"Q: SR Latch {SRLatch.__counter}", maxOutSize=1, delay=0, plot=plot)
        o = pydig.combinationalFromObject(self)
        self.__o_not = pydig.combinational(maxOutSize=1, plot=False, blockID=f"~Q: SR Latch {SRLatch.__counter}", func=lambda x: x, delay=0)
        n1 = pydig.combinational(maxOutSize=1, plot=False, blockID=f"N1 SR {SRLatch.__counter}", func=lambda x: SRLatch.__nor(x >> 1 & 1, x & 1), delay=0.1)
        n2 = pydig.combinational(maxOutSize=1, plot=False, blockID=f"N2 SR {SRLatch.__counter}", func=lambda x: SRLatch.__nor(x >> 1 & 1, x & 1), delay=0.1)

        SR.output(0, 1) > n1.input()
        n2.output() > n1.input()
        n1.output() > n2.input()
        SR.output(1, 2) > n2.input()

        n1.output() > o.input()
        n2.output() > self.__o_not.input()

    @staticmethod
    def __nor(a, b):
        """
        @param a : input signal
        """
        return (~(a | b)) & 0b1

    def getQNot(self):
        """
        @return Combinational : the ~Q output
        """
        return self.__o_not


class DLatch(Comb):
    __counter = 0

    def __init__(self, pydig: pd, clk: Clock, D: HOC, plot: bool = True):
        """
        @param pydig : pydig object
        @param clk : the clock signal
        @param D : the data signal
        @param plot : boolean value whether to plot this moore machine or not
        """
        checkType([(pydig, pd), (clk, Clock), (D, HOC), (plot, bool)])

        DLatch.__counter += 1

        Comb.__init__(self, func=lambda x: x, env=pydig.getEnv(), blockID=f"Q: D Latch {DLatch.__counter}", maxOutSize=1, delay=0, plot=plot)
        o = pydig.combinationalFromObject(self)
        self.__o_not = pydig.combinational(maxOutSize=1, plot=False, blockID=f"~Q: D Latch {DLatch.__counter}", func=lambda x: x, delay=0)

        D_not = pydig.combinational(maxOutSize=1, plot=False, blockID=f"D Not D {DLatch.__counter}", func=lambda x: (DLatch.__not(x)), delay=0)
        R = pydig.combinational(maxOutSize=1, plot=False, blockID=f"R D {DLatch.__counter}", func=lambda x: (x >> 1) & (x & 1), delay=0)
        S = pydig.combinational(maxOutSize=1, plot=False, blockID=f"S D {DLatch.__counter}", func=lambda x: (x >> 1) & (x & 1), delay=0)

        SR = pydig.combinational(maxOutSize=1, plot=False, blockID=f"SR D {DLatch.__counter}", func=lambda x: x, delay=0)

        self.__clk = clk

        D.output() > D_not.input()

        clk.output() > R.input()
        D_not.output() > R.input()

        clk.output() > S.input()
        D.output() > S.input()

        R.output() > SR.input()
        S.output() > SR.input()

        SRLatch1 = SRLatch(pydig, SR, plot=False)
        SRLatch1.output() > o.input()
        SRLatch1.getQNot().output() > self.__o_not.input()

    def getQNot(self):
        """
        @return Combinational : the ~Q output
        """
        return self.__o_not

    @staticmethod
    def __not(x):
        """
        @param x : the input signal
        """
        return (~x) & 0b1
    
    def getScopeDump(self):
        """
        @return : the scope dump values for this block.
        """
        dic = self.__clk.getScopeDump()
        dic.update(self._scopeDump.getValues())
        return dic


if __name__ == "__main__":

    pydig = pd()
    i = pydig.source(filePath="Tests\\DLatch.csv", plot=False, blockID=f"D Latch")
    clk = pydig.clock(plot=False, blockID="Clock", timePeriod=6, onTime=3, initialValue = 1)
    output1 = DLatch(pydig, clk, i, plot=True)

    pydig.generateCSV()
    pydig.run(until=30)
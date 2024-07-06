import os
import sys
from DifferentRegisters import SIPO
# directory reach
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from utilities import checkType, bitCount, printErrorAndExit
from pydig import pydig as pd


class StraightRingCounter():

  def __init__(self, pydig: pd, size:int, clock, plot: bool, blockID: str):

    self.__register = SIPO(pydig, size, clock, 0.01, 2**(size-1), plot, blockID)
    self.__register.output() > self.__register.input()

  def input(self, left=None, right=None):
    printErrorAndExit("No input allowed for ring counters")
    
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
      self.__register.clock() <= other
      return True

  def __gt__(self,other):
      self.__register.output() > other
      return True

class JohnsonCounter():

  def __init__(self, pydig: pd, size:int, clock, plot: bool, blockID: str):

    self.__register = SIPO(pydig, size, clock, 0.01, 0, plot, blockID)
    self.__not = pydig.combinational(maxOutSize = 1, plot=False, blockID = blockID+"'s NOT Gate", func=lambda x: (1-(x&1))&1, delay=0.01, initialValue=0)
    self.__register.output(0,1) > self.__not.input()
    self.__not.output() > self.__register.input()

  def input(self, left=None, right=None):
    printErrorAndExit("No input allowed for ring counters")
    
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
      self.__register.clock() <= other
      return True

  def __gt__(self,other):
      self.__register.output() > other
      return True


if __name__ == "__main__":
  
  pysim = pd("Ring Counters")
  clock = pysim.clock(plot=True, onTime=0.5, timePeriod=1, initialValue = 1)
  src = StraightRingCounter(pysim, 4, clock, True, "src")
  o1 = pysim.output(plot = True,blockID = "o1")
  jrc = JohnsonCounter(pysim, 4, clock, True, "jrc")
  o2 = pysim.output(plot = True, blockID = "o2")
  src > o1
  jrc > o2
  
  pysim.run(20)

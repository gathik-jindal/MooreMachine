import os
import sys

# directory reach
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from utilities import checkType, bitCount, printErrorAndExit
from pydig import pydig as pd
from DifferrentRegisters import SIPO

class StraightRingCounter():

  def __init__(self,pydig: pd, size:int, clock, delay: float, plot: bool, blockID: str):

    self.__register = SIPO(pd, size, clock, delay, 0.01, plot, blockID)
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

  def __init__(self,pydig: pd, size:int, clock, delay: float, plot: bool, blockID: str):

    self.__register = SIPO(pydid, size, clock, delay, 0.01, plot, blockID)
    self.__not = pydig.combinational(1, plot=False, blockID+"'s NOT Gate", func=lambda x: (1-(x&1))&1, delay=0.01, initialValue=0):
    self.__register.output() > self.__not.input()
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

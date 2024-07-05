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


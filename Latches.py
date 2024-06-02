from blocks import Combinatorics as Comb, HasOutputConnections as HOC
from blocks import pydig as pd
from utilities import checkType

class SRLatch(Comb):
    __counter = 0

    def __init__(self, pydig:pd, SR:HOC, plot:bool = True):
        checkType([(pydig, pd), (SR, HOC), (plot, bool)])

        SRLatch.__counter += 1

        Comb.__init__(self, func = lambda x : x, env = pydig.getEnv(), blockID = f"Q: SR Latch {SRLatch.__counter}", maxOutSize = 1, delay = 0, plot = plot)
        o = pydig.combinatoricsFromObject(self)
        self.__o_not = pydig.combinatorics(maxOutSize = 1, plot = False, blockID = f"~Q: SR Latch {SRLatch.__counter}", func = lambda x : x, delay = 0)
        n1 = pydig.combinatorics(maxOutSize = 1, plot = False, blockID = f"N1 SR {SRLatch.__counter}", func = lambda x : SRLatch.__nor(x >> 1 & 1, x & 1), delay = 0.1)
        n2 = pydig.combinatorics(maxOutSize = 1, plot = False, blockID = f"N2 SR {SRLatch.__counter}", func = lambda x : SRLatch.__nor(x >> 1 & 1, x & 1), delay = 0.1)

        SR.output(0, 1) > n1.input()
        n2.output() > n1.input()
        n1.output() > n2.input()
        SR.output(1, 2) > n2.input()

        n1.output() > o.input()
        n2.output() > self.__o_not.input()

    @staticmethod
    def __nor(a, b):
        return (~(a | b)) & 0b1
    
    def getQNot(self):
        return self.__o_not

class DLatch(Comb):
    __counter = 0

    def __init__(self, pydig:pd, CLK_D:HOC, plot:bool = True):
        checkType([(pydig, pd), (CLK_D, HOC), (plot, bool)])

        DLatch.__counter += 1

        Comb.__init__(self, func = lambda x : x, env = pydig.getEnv(), blockID = f"Q: D Latch {DLatch.__counter}", maxOutSize = 1, delay = 0, plot = plot)
        o = pydig.combinatoricsFromObject(self)
        self.__o_not = pydig.combinatorics(maxOutSize = 1, plot = False, blockID = f"~Q: D Latch {DLatch.__counter}", func = lambda x : x, delay = 0)

        clk = pydig.combinatorics(maxOutSize = 1, plot = False, blockID = f"Clock D {DLatch.__counter}", func = lambda x : (x >> 1 & 1), delay = 0)
        D = pydig.combinatorics(maxOutSize = 1, plot = False, blockID = f"D D {DLatch.__counter}", func = lambda x : (x & 1), delay = 0)
        D_not = pydig.combinatorics(maxOutSize = 1, plot = False, blockID = f"D Not D {DLatch.__counter}", func = lambda x : (DLatch.__not(x)), delay = 0)
        R = pydig.combinatorics(maxOutSize = 1, plot = False, blockID = f"R D {DLatch.__counter}", func = lambda x : (x >> 1) & (x & 1), delay = 0)
        S = pydig.combinatorics(maxOutSize = 1, plot = False, blockID = f"S D {DLatch.__counter}", func = lambda x : (x >> 1) & (x & 1), delay = 0)

        SR = pydig.combinatorics(maxOutSize = 1, plot = False, blockID = f"SR D {DLatch.__counter}", func = lambda x : x, delay = 0)
        
        CLK_D.output() > clk.input()
        CLK_D.output() > D.input()
        D.output() > D_not.input()

        clk.output() > R.input()
        D_not.output() > R.input()

        clk.output() > S.input()
        D.output() > S.input()

        R.output() > SR.input()
        S.output() > SR.input()

        SRLatch1 = SRLatch(pydig, SR, plot = False)
        SRLatch1.output() > o.input()
        SRLatch1.getQNot().output() > self.__o_not.input()
    
    def getQNot(self):
        return self.__o_not

    @staticmethod
    def __not(x):
        return (~x) & 0b1
    
if __name__ == "__main__":

    pydig = pd()
    i = pydig.source(filePath = "Tests\\DLatch.csv", plot = False, blockID = f"D Latch")
    output1 = DLatch(pydig, i, plot = True)
    
    pydig.generateCSV()
    pydig.run(until = 30)

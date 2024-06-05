from blocks import pydig as pd
from blocks import Clock as Clock
from utilities import checkType

class EnabledBit2CounterWithTC:

    def __init__(self, pydig:pd, clk:Clock, inputObject, blockID, left = 0, right = None):
        
        self.__i = inputObject
        self.__m = pydig.moore(maxOutSize = 3, plot = True, blockID = blockID)
        
        # Assigning the different components
        self.__m.nsl = self.nsl
        self.__m.ol = self.ol
        
        # Making all the connections
        self.__i.output(left, right) > self.__m.input()
        clk.output() > self.__m.clock()
    
    @staticmethod
    def nsl(ps, en):
        a = en
        b = (ps >> 1) & 1
        c = ps & 1
        
        d = ~a&b | b&~c | a&~b&c
        e = a ^ c
        return d << 1 | e 

    @staticmethod
    def ol(ps):
        f = (ps >> 1) & 1
        g = ps & 1

        return f << 2 | g << 1 | f & g
    
    def getMachine(self):
        return self.__m
    
    def getOutput(self):
        return self.__m

class EnabledBit4CounterWithTC:

    def __init__(self, pydig:pd, clk:Clock, inputObject, blockID1, blockID2):
        
        self.__bit2Counter1 = EnabledBit2CounterWithTC(pydig, clk, inputObject, blockID1).getMachine()
        self.__bit2Counter2 = EnabledBit2CounterWithTC(pydig, clk, self.__bit2Counter1, blockID2, left = 0, right = 1).getMachine()
        
    def getMachine(self):
        return (self.__bit2Counter1, self.__bit2Counter2)

if __name__ == "__main__":
    pydig = pd()

    inputObject = pydig.source("Tests\\BitCounter.csv", plot = True, blockID = "input")
    clk = pydig.clock(blockID= "clk", plot = True, timePeriod = 1, onTime = 0.5)

    m1, m2 = EnabledBit4CounterWithTC(pydig, clk, inputObject, "2 Bit Counter 1", "2 Bit Counter 2").getMachine()
    o = pydig.output(blockID = "Output")

    m1.output(1, 3) > o.input()
    m2.output(1, 3) > o.input()
    pydig.generateCSV()

    # Running all the blocks.
    pydig.run(until = 30)

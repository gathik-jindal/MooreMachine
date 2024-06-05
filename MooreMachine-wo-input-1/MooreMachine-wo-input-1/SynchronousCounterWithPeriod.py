from blocks import pydig as pd
from blocks import Clock as Clock, Combinatorics as Comb
from utilities import checkType, printErrorAndExit

class SynchronousCounterWithPeriod(Comb):

    __counter = 0

    def __init__(self, pydig:pd, modValue:int, period:int, clock:Clock, plot:bool = True):
        
        checkType([(pydig, pd), (modValue, int), (clock, Clock), (plot, bool), (period, int)])
        maxOutSize = SynchronousCounterWithPeriod.__bitCount(modValue)
        self.__modValue = modValue
        SynchronousCounterWithPeriod.__counter += 1

        if(period >= modValue or period <= 0):
            printErrorAndExit(f"Period {period} must be between 1 and {modValue}")

        Comb.__init__(self, func = lambda x : x, env = pydig.getEnv(), blockID = f"Mod {modValue} Period {period} Counter {SynchronousCounterWithPeriod.__counter}", 
                maxOutSize = maxOutSize, delay = 0, plot = plot, state = 0)
        
        o = pydig.combinatoricsFromObject(self)
        m = pydig.moore(plot = False, maxOutSize = maxOutSize, blockID = f"Moore {SynchronousCounterWithPeriod.__counter}")
        equal = pydig.combinatorics(maxOutSize = 1, plot = False, blockID = f"Equality Comparator {SynchronousCounterWithPeriod.__counter}", 
                                    func = lambda x : int(x == period), delay = 0, state = 0)
        clk = clock
        
        m.nsl = self.__nsl
        m.ol = self.__ol

        equal.output() > m.input()
        clk.output() > m.clock()
        m.output() > o.input()
        m.output() > equal.input()
    
    @staticmethod
    def __bitCount(num):
        a = 0
        while(num):
            a+=1
            num = num >> 1
        return a
    
    def __nsl(self, ps, i):
        if(i == 1):
            return 0
        return (ps + 1) % self.__modValue
    
    def __ol(self, ps):
        return ps


if __name__ == "__main__":

    pydig = pd()
    clock = pydig.clock(blockID = "", plot = False, timePeriod = 1, onTime = 0.5)
    output1 = SynchronousCounterWithPeriod(pydig, 6 , 4, clock, plot = True)
    
    pydig.generateCSV()
    pydig.run(until = 30)

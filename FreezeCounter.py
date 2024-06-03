from blocks import pydig as pd
from blocks import Clock as Clock, Combinatorics as Comb, HasOutputConnections as HOC
from utilities import checkType

class FreezeCounter(Comb):

    __counter = 0

    def __init__(self, pydig:pd, modValue:int, syncReset:HOC, clock:Clock, plot:bool = True):
        
        checkType([(pydig, pd), (modValue, int), (syncReset, HOC), (clock, Clock), (plot, bool)])
        maxOutSize = FreezeCounter.__bitCount(modValue)
        self.__modValue = modValue
        FreezeCounter.__counter += 1

        Comb.__init__(self, func = lambda x : x, env = pydig.getEnv(), blockID = f"Mod {modValue} Freeze Counter {FreezeCounter.__counter}", 
                maxOutSize = maxOutSize, delay = 0, plot = plot, state = 0)
        
        o = pydig.combinatoricsFromObject(self)
        i = syncReset
        m = pydig.moore(plot = False, maxOutSize = maxOutSize, blockID = f"Moore {FreezeCounter.__counter}")
        clk = clock
        
        m.nsl = self.__nsl
        m.ol = self.__ol

        i.output() > m.input()
        clk.output() > m.clock()
        m.output() > o.input()
    
    @staticmethod
    def __bitCount(num):
        a = 0
        while(num):
            a+=1
            num = num >> 1
        return a
    
    def __nsl(self, ps, i):
        if(i == 1):
            return ps
        return (ps + 1) % self.__modValue
    
    def __ol(self, ps):
        return ps


if __name__ == "__main__":

    pydig = pd()
    clock = pydig.clock(blockID = "", plot = False, timePeriod = 1, onTime = 0.5)
    i = pydig.source(filePath = "Tests\\FreezeCounter.csv", plot = False, blockID = f"Sync Reset")
    output1 = FreezeCounter(pydig, 6 , i, clock, plot = True)
    
    pydig.generateCSV()
    pydig.run(until = 30)

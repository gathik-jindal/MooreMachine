from blocks import pydig as pd
from utilities import checkType

class SynchronusCounter:

    def __init__(self, pydig:pd, modValue:int, asyncReset:str, timePeriod:float = 1, onTime:float = 0.5):
        checkType([(pydig, pd), (modValue, int), (asyncReset, str), (timePeriod, (int, float)), (onTime, (int, float))])

        self.__modValue = modValue

        self.__i = pydig.source(asyncReset, "Async Reset")
        self.__m = pydig.moore(plot = True, blockID = f"Mod {modValue} Counter") 
        self.__o = pydig.output(plot = False, blockID = "Final Output")
        self.__clk = pydig.clock(blockID= "", timePeriod = timePeriod, onTime = onTime)
        
        self.__m.nsl = self.nsl
        self.__m.ol = self.ol

        self.__i.output() > self.__m.input()
        self.__clk.output() > self.__m.clock()
        self.__m.output() > self.__o.input()
        
    def nsl(self, ps, i):
        if(i == 1):
            return 0
        return (ps + 1) % self.__modValue
    
    def ol(self, ps):
        return ps

    def getOutput(self):
        return self.__o

if __name__ == "__main__":

    pydig = pd()
    SynchronusCounter(pydig, 6, "Tests\\SyncCounter.csv")

    pydig.dumpVars()
    pydig.run(until = 30)
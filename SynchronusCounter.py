from blocks import pydig as pd
from utilities import checkType

class SynchronusCounter:

    def __init__(self, modValue:int, asyncReset:str, run:float, timePeriod:float = 1, onTime:float = 0.5):
        checkType([(modValue, int), (asyncReset, str), (run, (int, float)), (timePeriod, (int, float)), (onTime, (int, float))])

        self.__pydig = pd()
        self.__modValue = modValue

        self.__i = self.__pydig.source(asyncReset, "Async Reset")
        self.__m = self.__pydig.moore(plot = True, blockID = f"Mod {modValue} Counter") 
        self.__clk = self.__pydig.clock(blockID= "", timePeriod = timePeriod, onTime = onTime)
        
        self.__m.nsl = self.nsl
        self.__m.ol = self.ol

        self.__i.output() > self.__m.input()
        self.__clk.output() > self.__m.clock()

        self.__pydig.dumpVars()
        self.__pydig.run(until = run)

    def nsl(self, ps, i):
        if(i == 1):
            return 0
        elif(ps + 1 == self.__modValue):
            return 0
        return ps + 1
    
    def ol(self, ps):
        return ps

if __name__ == "__main__":
    SynchronusCounter(6, "Tests\\SyncCounter.csv", 30)
                                                            
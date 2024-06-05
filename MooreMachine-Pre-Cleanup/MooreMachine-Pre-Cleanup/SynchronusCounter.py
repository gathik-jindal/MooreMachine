from blocks import pydig as pd
from blocks import Clock as Clock
from utilities import checkType

class SynchronusCounter:

    def __init__(self, pydig:pd, modValue:int, syncReset:str, clock:Clock):
        checkType([(pydig, pd), (modValue, int), (syncReset, str), (clock, Clock)])

        self.__modValue = modValue
        self.__i = pydig.source(syncReset, True, "Async Reset")
        self.__m = pydig.moore(plot = True, maxOutSize = self.__bitCount(modValue), blockID = f"Mod {modValue} Counter") 
        self.__o = pydig.output(plot = False, blockID = "Final Output")
        self.__clk = clock
        
        self.__m.nsl = self.nsl
        self.__m.ol = self.ol

        self.__i.output() > self.__m.input()
        self.__clk.output() > self.__m.clock()
        self.__m.output() > self.__o.input() ####### make combinatorics

    def __bitCount(self, num):
        a = 0
        while(num):
            a+=1
            num = num >> 1
        return a
    
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
    clock = pydig.clock(blockID = "", timePeriod = 1, onTime = 0.5)
    output1 = SynchronusCounter(pydig, 6 , "Tests\\SyncCounter.csv", clock).getOutput()
    print(output1)
    
    pydig.generateCSV()
    pydig.run(until = 30)

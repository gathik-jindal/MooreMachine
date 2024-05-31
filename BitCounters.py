from blocks import pydig as pd
from blocks import Clock as Clock, Combinatorics as Comb, HasOutputConnections as HOC
from utilities import checkType

class Enabled1BitCounterWithTC(Comb):
    
    __counter = 0

    def __init__(self, pydig:pd, syncReset:HOC, clock:Clock, plot:bool = True):
        checkType([(pydig, pd), (syncReset, HOC), (clock, Clock), (plot, bool)])

        Enabled1BitCounterWithTC.__counter += 1

        Comb.__init__(self, func = lambda x : x & 1, env = pydig.getEnv(), blockID = f"Enabled 1 Bit Counter {Enabled1BitCounterWithTC.__counter}", 
                maxOutSize = 1, delay = 0, plot = plot, state = 0)
        
        o = pydig.combinatoricsFromObject(self)
        self.__tc = pydig.combinatorics(maxOutSize = 1, plot = False, blockID = f"Enabled 1 Bit Counter TC{Enabled1BitCounterWithTC.__counter}", 
                                    func = lambda x : (x & 2) >> 1)
        i = syncReset
        m = pydig.moore(plot = False, maxOutSize = 2, blockID = f"Moore {Enabled1BitCounterWithTC.__counter}")
        clk = clock

        m.nsl = self.__nsl
        m.ol = self.__ol

        i.output() > m.input()
        clk.output() > m.clock()
        m.output() > o.input()
        m.output() > self.__tc.input()
    
    def __nsl(self, ps, i):
        return ps ^ i

    def __ol(self, ps):
        # TC, Output
        return ps << 1 | ps
    
    def getTerminalCount(self):
        return self.__tc

class Enabled2BitCounterWithTC(Comb):

    __counter = 0

    def __init__(self, pydig:pd, syncReset:HOC, clock:Clock, plot:bool = True):
        checkType([(pydig, pd), (syncReset, HOC), (clock, Clock), (plot, bool)])
        
        Enabled2BitCounterWithTC.__counter += 1
        
        self.__c1 = Enabled1BitCounterWithTC(pydig, syncReset, clock, plot = False)

        temp = pydig.combinatorics(maxOutSize = 1, plot = False, blockID = f"Enabled 2 Bit Counter And{Enabled2BitCounterWithTC.__counter}", 
                                    func = lambda x : (x >> 1 & 1) & (x & 1))

        self.__c2 = Enabled1BitCounterWithTC(pydig, temp.output(), clock, plot = False)

        Comb.__init__(self, func = lambda x : x, env = pydig.getEnv(), blockID = f"Enabled 2 Bit Counter {Enabled2BitCounterWithTC.__counter}", 
                maxOutSize = 2, delay = 0, plot = plot, state = 0)
        o = pydig.combinatoricsFromObject(self)
        self.__tc = pydig.combinatorics(maxOutSize = 1, plot = False, blockID = f"Enabled 2 Bit Counter TC{Enabled2BitCounterWithTC.__counter}", 
                                    func = lambda x : (x >> 1 & 1) & (x & 1))
        
        self.__c1.output() > o.input()
        self.__c2.output() > o.input()
        syncReset.output() > temp.input()
        self.__c1.getTerminalCount().output() > temp.input()
        self.__c1.getTerminalCount().output() > self.__tc.input()
        self.__c2.getTerminalCount().output() > self.__tc.input()
    
    def getTerminalCount(self):
        return self.__tc

class Enabled3BitCounterWithTC(Comb):

    __counter = 0

    def __init__(self, pydig:pd, syncReset:HOC, clock:Clock, plot:bool = True):
        checkType([(pydig, pd), (syncReset, HOC), (clock, Clock), (plot, bool)])
        
        Enabled3BitCounterWithTC.__counter += 1
        
        self.__c1 = Enabled1BitCounterWithTC(pydig, syncReset, clock, plot = False)

        temp = pydig.combinatorics(maxOutSize = 1, plot = False, blockID = f"Enabled 3 Bit Counter And{Enabled3BitCounterWithTC.__counter}", 
                                    func = lambda x : (x >> 1 & 1) & (x & 1))

        self.__c2 = Enabled2BitCounterWithTC(pydig, temp.output(), clock, plot = False)

        Comb.__init__(self, func = lambda x : x, env = pydig.getEnv(), blockID = f"Enabled 3 Bit Counter {Enabled3BitCounterWithTC.__counter}", 
                maxOutSize = 3, delay = 0, plot = plot, state = 0)
        o = pydig.combinatoricsFromObject(self)
        self.__tc = pydig.combinatorics(maxOutSize = 1, plot = False, blockID = f"Enabled 3 Bit Counter TC{Enabled3BitCounterWithTC.__counter}", 
                                    func = lambda x : (x >> 1 & 1) & (x & 1))
        
        self.__c1.output() > o.input()
        self.__c2.output() > o.input()
        syncReset.output() > temp.input()
        self.__c1.getTerminalCount().output() > temp.input()
        self.__c1.getTerminalCount().output() > self.__tc.input()
        self.__c2.getTerminalCount().output() > self.__tc.input()
    
    def getTerminalCount(self):
        return self.__tc

class Enabled4BitCounterWithTC(Comb):

    __counter = 0

    def __init__(self, pydig:pd, syncReset:HOC, clock:Clock, plot:bool = True):
        checkType([(pydig, pd), (syncReset, HOC), (clock, Clock), (plot, bool)])
        
        Enabled4BitCounterWithTC.__counter += 1
        
        self.__c1 = Enabled2BitCounterWithTC(pydig, syncReset, clock, plot = False)

        temp = pydig.combinatorics(maxOutSize = 1, plot = False, blockID = f"Enabled 4 Bit Counter And{Enabled4BitCounterWithTC.__counter}", 
                                    func = lambda x : (x >> 1 & 1) & (x & 1))

        self.__c2 = Enabled2BitCounterWithTC(pydig, temp.output(), clock, plot = False)

        Comb.__init__(self, func = lambda x : x, env = pydig.getEnv(), blockID = f"Enabled 4 Bit Counter {Enabled4BitCounterWithTC.__counter}", 
                maxOutSize = 4, delay = 0, plot = plot, state = 0)
        o = pydig.combinatoricsFromObject(self)
        self.__tc = pydig.combinatorics(maxOutSize = 1, plot = False, blockID = f"Enabled 4 Bit Counter TC{Enabled4BitCounterWithTC.__counter}", 
                                    func = lambda x : (x >> 1 & 1) & (x & 1))
        
        self.__c1.output() > o.input()
        self.__c2.output() > o.input()
        syncReset.output() > temp.input()
        self.__c1.getTerminalCount().output() > temp.input()
        self.__c1.getTerminalCount().output() > self.__tc.input()
        self.__c2.getTerminalCount().output() > self.__tc.input()
    
    def getTerminalCount(self):
        return self.__tc

if __name__ == "__main__":

    pydig = pd()
    clock = pydig.clock(blockID = "", plot = False, timePeriod = 1, onTime = 0.5)
    input1 = pydig.source(filePath = "Tests\\BitCounter.csv", plot = False, blockID = "Input")
    output1 = Enabled4BitCounterWithTC(pydig , input1, clock, plot = True)
    
    pydig.generateCSV()
    pydig.run(until = 60)

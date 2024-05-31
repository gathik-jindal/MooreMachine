from blocks import pydig


#First two bits are Period and next two bits are Compare
#Tperiod = (Period + 1) * Tclk
#Ton = Compare * Tclk

def n(a):
    return (~a&0b1)

def nsl(ps, i):
    a = (ps >> 1) & 1
    b = (ps >> 0) & 1

    d = (n(a) & b & n(i)) | (a & n(b) & n(i))
    e = (n(b) & n(i))

    return d << 1 | e

def ol(ps):
    return ps

pd = pydig()

#Creating the input Objects
PWM_Path = "Tests\\PWM.csv"
PWM_Input = pd.source(filePath = PWM_Path, plot = True, blockID = "PWM Input")
period = pd.combinatorics(maxOutSize = 2, plot = False, blockID = "Period", func = lambda x : x >> 2, delay = 0)
compare = pd.combinatorics(maxOutSize = 2, plot = False, blockID = "Compare", func = lambda x: x & 3, delay = 0)

#Creating the clock
clk = pd.clock(plot = True, blockID = "Clock", timePeriod = 1, onTime = 0.5)

#Creating the comparators
syncResetComparator = pd.combinatorics(maxOutSize = 1, plot = False, blockID = "Sync Reset Comparator", 
                                       func = lambda x : int((x & 3) == (x >> 2)), delay = 0)
outputComparator = pd.combinatorics(maxOutSize = 1, plot = False, blockID = "Output Comparator", 
                                        func = lambda x : int((x & 3) > (x >> 2)), delay = 0)


#Creating the moore machine
mod4Counter = pd.moore(maxOutSize = 2, plot = True, blockID = "Mod 4 Counter", startingState = 0)
mod4Counter.nsl = nsl
mod4Counter.ol = ol

#Final output object
finalOutput = pd.output(plot = True, blockID = "PWM Output")

#Creating the connections
PWM_Input.output() > period.input()
PWM_Input.output() > compare.input()

compare.output() > outputComparator.input()
mod4Counter.output() > outputComparator.input()

period.output() > syncResetComparator.input()
mod4Counter.output() > syncResetComparator.input()

outputComparator.output() > finalOutput.input()

syncResetComparator.output() > mod4Counter.input()
clk.output() > mod4Counter.clock()

pd.generateCSV()
pd.run(until = 40)
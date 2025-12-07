import pydig

pysim = pydig.pydig(name = "Pydig")

def n(a):
    return (~a & 0b1)

def nsl(ps, i):
    a = (ps >> 1) & 1
    b = (ps >> 0) & 1
    d = (n(a) & b & n(i)) | (a & n(b) & n(i))
    e = (n(b) & n(i))
    return d << 1 | e

def ol(ps):
    return ps


input0 = pysim.source(filePath = "Tests\\PWM.csv", plot = False, blockID = "PWM Input")
clock1 = pysim.clock(plot = False, blockID = "clk", timePeriod = 1, onTime = 0.5, initialValue = 0)
moore2 = pysim.moore(maxOutSize = 2, plot = True, blockID = "Mod 4 Counter", nsl = nsl, ol = ol, startingState = 0, risingEdge = True, nsl_delay = 0.01, ol_delay = 0.01, register_delay = 0.01)
comb3 = pysim.combinational(maxOutSize = 1, plot = False, blockID = "Sync Reset Comparator", func = lambda x: int((x & 3) == (x >> 2)), delay = 0, initialValue = 0)
comb4 = pysim.combinational(maxOutSize = 1, plot = False, blockID = "Output Comparator", func = lambda x: int((x & 3) > (x >> 2)), delay = 0, initialValue = 0)
output5 = pysim.output(plot = True, blockID = "PWM Output")
input0.output(0, 2) > comb4.input()
moore2.output() > comb4.input()
input0.output(2, 4) > comb3.input()
moore2.output() > comb3.input()
comb3.output() > moore2.input()
comb4.output() > output5.input()
clock1.output() > moore2.clock()
pysim.generateCSV()
pysim.run(until = 40)

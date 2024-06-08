import pydig

pysim = pydig.pydig(name = "Pydig")

def n(a):

    # This is the logic of a single input not gate
    return (~a & 0b1)


def nsl(ps, i):

    # This is the Next State Logic for the PWM

    a = (ps >> 1) & 1
    b = (ps >> 0) & 1

    d = (n(a) & b & n(i)) | (a & n(b) & n(i))
    e = (n(b) & n(i))

    return d << 1 | e


def ol(ps):

    # This is the output logic for the PWM
    return ps

input0 = pysim.source(filePath = "C:\\Users\\ARYAN\\Desktop\\Moore Machine Simulator\\Tests\\PWM.csv", plot = False, blockID = "PWM Input")
clock1 = pysim.clock(plot = False, blockID = "clk", timePeriod = 1.2, onTime = 0.6, initialValue = 0)
moore2 = pysim.moore(maxOutSize = 2, plot = True, blockID = "Mod 4 Counter", nsl = nsl, ol = ol, startingState = 0)
comb3 = pysim.combinational(maxOutSize = 1, plot = False, blockID = "Output Comparator", func = lambda x: int((x & 3) > (x >> 2)), delay = 0, initialValue = 0)
output4 = pysim.output(plot = True, blockID = "PWM Output")
comb5 = pysim.combinational(maxOutSize = 1, plot = False, blockID = "Sync Reset Comparator", func = lambda x: int((x & 3) == (x >> 2)), delay = 0, initialValue = 0)
comb5.output() > moore2.input()
clock1.output() > moore2.clock()
input0.output(0, 2) > comb3.input()
moore2.output() > comb3.input()
input0.output(2, 4) > comb5.input()
moore2.output() > comb5.input()
comb3.output() > output4.input()
pysim.generateCSV()
pysim.run(until = 40)

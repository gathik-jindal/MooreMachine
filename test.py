from blocks import pydig

def n(a):
    return (~a&0b1)

pd = pydig()

clk = pd.clock(plot = True, blockID = "Clock", timePeriod = 1, onTime = 0.5)
machine = pd.moore(maxOutSize=1, plot=True, nsl=lambda x, y : n(y), ol = lambda y : y)

# machine.clock()
machine.input()
clk.output() > machine.clock()
clk.output() > machine.input()

pd.generateCSV()

pd.run(until=30)
from blocks import pydig

pd = pydig()

clk = pd.clock(plot = True, blockID = "Clock", timePeriod = 1, onTime = 0.5)
machine = pd.moore(maxOutSize=1, plot=True, nsl=lambda x, y : x+y, ol = lambda y : y)

clk.output() > machine.input()
clk.output(input = 1) > machine.input()

pd.generateCSV()

pd.run(until=30)
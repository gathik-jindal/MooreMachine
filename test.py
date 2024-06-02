from blocks import pydig

pd = pydig()

clk = pd.clock(plot = True, blockID = "Clock", timePeriod = 1, onTime = 0.5)
combi = pd.combinatorics(maxOutSize=1, plot=True, blockID="Combinatorics", func=lambda x: x, delay=0.2)

clk.output(input=True) > combi.input()

pd.run(until=30)
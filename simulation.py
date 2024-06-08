import pydig

pysim = pydig.pydig(name = "Pydig")



output0 = pysim.output(plot = False, blockID = "Output Block")
comb1 = pysim.combinational(maxOutSize = 1, plot = False, blockID = "Combinational Block", func = lambda x: x, delay = 0, initialValue = 0)
input3 = pysim.source(filePath = "filePath", plot = False, blockID = "Input Block")

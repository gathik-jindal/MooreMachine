import pwlSource

inputGen = pwlSource.InputGenerator("Tests\\Test.csv")
inputs = inputGen.getInput()
print(inputs)

inputGen.setFilePath("Tests\\Test.txt")
inputs = inputGen.getInput()
print(inputs)

inputGen.setFilePath("Tests\\Test.xlsx")
inputs = inputGen.getInput()
print(inputs)

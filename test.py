import pwlSource

inputGen = pwlSource.InputGenerator("Tests\\Test.csv")
print("-----printing .csv-------")
inputs = inputGen.getInput()
print(inputs)

inputGen.setFilePath("Tests\\Test.txt")
print("-----printing .txt-------")
inputs = inputGen.getInput()
print(inputs)

inputGen.setFilePath("Tests\\Test.xlsx")
print("-----printing .xlsx------")
inputs = inputGen.getInput()
print(inputs)

import pwlSource
from scope import plot

plot_dict = {}

inputGen = pwlSource.InputGenerator("Tests\\Test.csv")
print("-----printing .csv-------")
inputs = inputGen.getInput()
print(inputs)
plot_dict['inputs_csv'] = inputs['Inputs']

inputGen.setFilePath("Tests\\Test.txt")
print("-----printing .txt-------")
inputs = inputGen.getInput()
print(inputs)
plot_dict['inputs_txt'] = inputs['Inputs']

inputGen.setFilePath("Tests\\Test.xlsx")
print("-----printing .xlsx------")
inputs = inputGen.getInput()
print(inputs)
plot_dict['inputs_excel'] = inputs['Inputs']

plot(plot_dict)
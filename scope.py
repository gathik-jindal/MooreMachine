"""
This class plots the waveforms that have been generated.
It requires that matplotlib has been already downloaded.
One can download matplotlib by
    pip install matplotlib

@author: Abhirath, Aryan, Gathik
@date: 31/12/2023
@version: 1.0
"""

from utilities import checkType, printErrorAndExit
from matplotlib import pyplot as plt

class Plotter:

    def __init__(self):
        pass

    def plot(self, inputs: dict, name: str):
        """
        plots the wave forms in a single window that are supplied in form of a dict.
        """
        
        # checking if data provided is correct
        checkType([(inputs, dict), (name, str)])
        for key in inputs:
            checkType([(key, str), (inputs[key], list)])

            for value in inputs[key]:
                checkType([(value, tuple)])

                if(len(value) == 2):
                    checkType([(value[0], (int, float)), (value[1], int)])
                else:
                    printErrorAndExit(f"{value} in {inputs[key]} in {inputs} is not of length 2.")

        # calculating max time
        maxTime = 0
        for key in inputs:
            time = [x[0] for x in inputs[key]]
            maxTime = int(max(maxTime, max(time) + 1))
        
        # finally plotting
        counter = 0
        done = 0
        numPlots = 0
        ticks = range(0, maxTime + 1)
        
        for key in inputs:    
            if(counter == 0):
                numPlots += 1
                fig, axs = plt.subplots(min(5, len(inputs) - done), 1, figsize=(8, 7.5), num = name + " #" + str(numPlots))

                if(len(inputs) - done == 1):
                    axs = [axs, None]
                
                fig.suptitle(name)

            time = [x[0] for x in inputs[key]]
            value = [y[1] for y in inputs[key]]

            if(not(0 in time)):
                value.insert(0, 0)
                time.insert(0, 0)
            if(not(maxTime in time)):
                value.insert(len(value), value[time.index((max(time)))])
                time.insert(len(time), maxTime)

            # Plot data on each subplot
            axs[counter].step(time, value, where = "post")
            axs[counter].grid(True)

            # formatting plots
            value = set(value)
            axs[counter].set_ylabel(key)
            axs[counter].set_yticks(range(0, max(value)+1))
            axs[counter].set_yticklabels([f"{x}" for x in range(0, max(value)+1)])
            axs[counter].set_ylim(bottom=0.0)

            axs[counter].set_xticks(ticks)
            axs[counter].set_xticklabels([f"{int(x)}" for x in ticks])
            axs[counter].set_xlim(left=0.0)
            axs[counter].sharex(axs[0])
            
            fig.tight_layout()

            counter += 1
            done += 1
            counter %= 5

    def show(self):
        """
        This function shows all the plots that have bee made
        """

        plt.show()

    @staticmethod
    def fillEmptyTimeSlots(timeValues:list, data:dict):
        """
        This functions makes sure that every element(list) in the dictionary has a value for every time unit.
        All the missing values are filled with the previous value.

        @return : a dictionary with the same keys but with the missing values filled.
        """

        timeCorresValues = [[] for x in timeValues]
        headerFields = []

        for i in data:
            headerFields.append(i)
            prevValue = 0 # the value of the previous time unit (for now zero)
            timePointer = 0

            for j in range(len(data[i])):
                if (timeValues[timePointer] < data[i][j][0]):
                    while (timeValues[timePointer] < data[i][j][0]):
                        timeCorresValues[timePointer].append(prevValue)
                        timePointer += 1
                    
                timeCorresValues[timePointer].append(data[i][j][1])
                timePointer += 1
                prevValue = data[i][j][1]
            
            while (timePointer < len(timeValues)):
                timeCorresValues[timePointer].append(prevValue)
                timePointer += 1
        
        # creating the dictionary
        finalData = {}
        
        for i in range(len(headerFields)):
            finalData[headerFields[i]] = [(timeValues[x], timeCorresValues[x][i]) for x in range(len(timeValues))]

        return finalData

if __name__ == "__main__":
    import pwlSource

    plot = Plotter()

    inputGen = pwlSource.InputGenerator("Tests\\Test.csv")
    print("-----printing .csv-------")
    inputs = inputGen.getInput()
    print(inputs)
    plot.plot(inputs, "CSV")

    inputGen.setFilePath("Tests\\Test.txt")
    print("-----printing .txt-------")
    inputs = inputGen.getInput()
    print(inputs)
    plot.plot(inputs, "TXT")

    inputGen.setFilePath("Tests\\Test.xlsx")
    print("-----printing .xlsx------")
    inputs = inputGen.getInput()
    print(inputs)
    plot.plot(inputs, "XLSX")

    # Remember to call this method at the end in order to show all the plots
    plot.show()

    

    # Incorrect ways to use the class
    # plot.plot(None, "Wrong")
    # plot.plot(inputs, None)
    # plot.plot(inputs, 2)
    # plot.plot(2, "Wrong")
    # plot.plot(None, None)

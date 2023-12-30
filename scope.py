"""
This class plots the waveforms that have been generated.
It requires that matplotlib has been already downloaded.
One can download matplotlib by
    pip install matplotlib

@author: Abhirath, Aryan, Gathik
@date: 17/12/2023
@version: 1.0
"""

from utilities import checkType, printErrorAndExit
from matplotlib import pyplot as plt
import sys
import numpy as np

class Plotter:

    def __init__(self):
        pass

    def __addNewFigure(self, name: str):
        """
        This function creates a new figure
        """

        plt.figure(name)

    def plot(self, inputs: dict, name: str):
        """
        plots the wave forms in a single window that are supplied in form of a dict.
        """
        
        checkType([(inputs, dict), (name, str)])

        maxTime = 0
        
        for key in inputs:
            time = [x[0] for x in inputs[key]]

            maxTime = int(max(maxTime, max(time) + 1))
        
        counter = 0
        
        ticks = np.linspace(0, maxTime, maxTime + 1)

        for key in inputs:
            
            if(counter == 0):
                fig, axs = plt.subplots(5, 1, figsize=(8, 7), sharex = True)
                fig.suptitle(name)

            time = [x[0] for x in inputs[key]]
            value = [y[1] for y in inputs[key]]

            # Plot data on each subplot
            axs[counter].step(time, value, where = "mid")
            axs[counter].grid(True)
            axs[counter].set_ylabel(key)
            axs[counter].set_yticks(value)
            axs[counter].set_yticklabels([f"{x}" for x in value])
            axs[counter].tick_params(axis='y', rotation=90)
            axs[counter].set_xticks(ticks)
            axs[counter].set_xticklabels([f"{int(x)}" for x in ticks])
            fig.tight_layout()

            counter += 1
            counter %= 5

    def show(self):
        """
        This function shows all the plots that have bee made
        """

        plt.show()

    def __printErrorAndExit(self, message: str):
        """
        This function prints the error message specified by message and exits. 
        """

        print(message)
        sys.exit(1)


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

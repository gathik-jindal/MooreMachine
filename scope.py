"""
This class plots the waveforms that have been generated.
It requires that matplotlib has been already downloaded.
One can download matplotlib by
    pip install matplotlib

@author: Abhirath, Aryan, Gathik
@date: 17/12/2023
@version: 1.0
"""

from matplotlib import pyplot as plt
import sys


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

        if (inputs == None or not (isinstance(inputs, dict))):
            self.__printErrorAndExit(f"{inputs} is not of type dict.")
        elif (name == None or not (isinstance(name, str))):
            self.__printErrorAndExit(f"{name} is not of type str.")

        self.__addNewFigure(name)

        n_rows = len(inputs)
        n_cols = 1

        plt.title('Waveforms')
        counter = 1
        for key in inputs:
            x_axis = [y[0] for y in inputs[key]]
            y_axis = [y[1] for y in inputs[key]]
            x_ticks = range(0, int(x_axis[-1]) + 1, 1)

            plt.subplot(n_rows, n_cols, counter)
            counter += 1
            plt.step(x_axis, y_axis, where='post')
            plt.ylabel(key)
            plt.xticks(x_ticks)
            plt.grid(True)

        plt.xlabel('Time (units)')
        plt.tight_layout()

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

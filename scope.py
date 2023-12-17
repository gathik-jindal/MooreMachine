"""
This class plots the waveforms that have been generated.
It requires that matplotlib has been already downloaded.
One can download matplotlib by
    pip install matplotlib

@author: Abhirath, Aryan, Gathik
@date: 13/12/2023
@version: 1.0
"""

from matplotlib import pyplot as plt

class Plotter:

    def __init__(self):
        pass
    
    def __addNewFigure(self, name:str):
        """
        This function creates a new figure
        """

        plt.figure(name)

    def plot(self, inputs: dict, name:str):
        """
        plots the wave forms in a single window that are supplied in form of a dict.
        """

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

    plot.show()
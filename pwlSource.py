"""
This class is used for getting input from the user.
The valid formats are txt, csv, and xlsx.
In order to use this class for reading xlsx, one needs to have pandas and openpyxl installed.
One can install pandas by the following method:
    pip install pandas
One can install openpyxl by the following method:
    pip install openpyxl

@author: Abhirath, Aryan, Gathik
@date: 13/12/2023
@version: 1.0
"""

class InputGenerator:

    def __init__(self, filePath:str):
        """
        filepath is the filepath of your txt, csv, or xslx file relative to this directory in str.
        """

        self.setFilePath(filePath)
    
    def setFilePath(self, filePath:str):
        """
        filepath is the filepath of your txt, csv, or xslx file relative to this directory in str.
        """
        
        try:
            if(filePath == None or not isinstance(filePath, str)):
                raise TypeError(f"File path \"{filePath}\" is not of type string.")

            self.__filePath = filePath

        except TypeError as e:
            print(e)
            exit()
    
    def getFilePath(self):
        return self.__filePath
    
    def getInput(self):
        """
        This function reads the input stored in the file specified by the given filePath.
        For txt files, the delimiter should be a space ' '
        For csv files, the delimiter should be a comma ','
        For xslx files, the delimeter should be a tab '\t'
        
        For txt files, the format should be as follows: 
            Input format that is expected in the file as follows:
            <time> <input>
            <time> <input>
            ...


            time should be convertible to float.
            input should be convertible to integer
        
        For csv files, the format should be as follows:
            TODO
        
        For xslx files, the format should be as follows:
            Input format is expected in the file as follows:
            Column:  A         B
                    Time     Input
                    <time>   <input>
                    <time>   <input>
                    <time>   <input>
                    ...


            time should be convertible to a float
            input should be convertible to integer   
        """

        try:
            if(self.__filePath.endswith(".csv")):
                return self.__openCsvFile()
            elif(self.__filePath.endswith(".txt")):
                return self.__openTxtFile()
            elif(self.__filePath.endswith(".xlsx")):
                return self.__openExcelFile()
            else:
                raise ValueError("File path is not of type csv, txt, or xslx.")
        
        except ValueError as e:
            print(e)
            exit()
    
    def __openCsvFile(self):
        pass
    
    def __openTxtFile(self):
        """
        This function reads inputs from a text file.

        Input format that is expected in the file as follows:
        <time> <input>
        <time> <input>
        ...


        time should be convertible to float.
        input should be convertible to integer
        """

        try:
            with open(self.__filePath, 'r') as fh:

                lines = fh.readlines()
                input_schedule = []

                for x in lines:

                    tu = x.split(" ")

                    if len(tu) != 2:
                        raise ValueError("Input Error: Corrupt input / Garbage input")

                    try:
                        input_schedule.append((float(tu[0]), int(tu[1])))
                    except ValueError:
                        print("Input Error: Inputs are not valid type")
                        exit()
        except IOError:
            print(f"The file path {self.__filePath} does not exist")
            exit()
        except ValueError as e:
            print(e)
            exit()

        return input_schedule

    def __openExcelFile(self):
        """
        This function reads input from an excel file.

        Input format is expected in the file as follows:
        Column:  A         B
                Time     Input
                <time>   <input>
                <time>   <input>
                <time>   <input>
                ...

        time should be convertible to a float
        input should be convertible to integer
        """
        import pandas as pd

        try:
            df = pd.read_excel(self.__filePath, usecols='A, B')
            values = df.to_dict()
            
            if(len(values) == 0):
                return []
            
            time, inputs = values.values()
            time = tuple(time.values())
            inputs = tuple(inputs.values())
            
            input_schedule = []

            try:
                time = tuple(map(float, time))
                inputs = tuple(map(int, inputs))
            except ValueError:
                print("Input Error: Inputs are not valid type")
                exit()
            
            input_schedule = list(map(lambda x, y: (x, y), time, inputs))
        except IOError:
            print(f"The file path {self.__filePath} does not exist")
            exit()
        
        return input_schedule

if __name__ == "__main__":

    #Correct ways for getting inputs
    #Note: Test.txt and Test.xlsx must be in the same directory
    fileInput = InputGenerator("Test\\Test.txt")
    inputs = fileInput.getInput()
    print(inputs)
    
    fileInput.setFilePath("Test\\Test.xlsx")
    inputs = fileInput.getInput()
    print(inputs)

    #Incorrect ways for getting inputs
    #It generates error message and exits

    #fileInput.setFilePath("Test1.txt")
    #inputs = fileInput.getInput()
    #print(inputs)
    
    #fileInput.setFilePath("Test1.xlsx")
    #inputs = fileInput.getInput()
    #print(inputs)

    #fileInput.setFilePath(2)
    #inputs = fileInput.getInput()
    #print(inputs)

    #fileInput.setFilePath(None)
    #inputs = fileInput.getInput()
    #print(inputs)
    
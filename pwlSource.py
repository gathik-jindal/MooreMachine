"""
This class is used for getting input from the user.
The valid formats are txt, csv, and xlsx.
In order to use this class for reading xlsx, one needs to have openpyxl installed.

@author: Abhirath, Aryan, Gathik
@date: 4/12/2023
@version: 1.6
"""

from utilities import checkType, printErrorAndExit
import pandas as pd

class InputGenerator:

    def __init__(self, filePath: str):
        """
        filepath is the filepath of your txt, csv, or xlsx file relative to this directory in str.
        """

        self.setFilePath(filePath)

    def __str__(self):
        """
        returns the linked file name
        """

        return f"The file linked is: {self.getFilePath()}"

    def setFilePath(self, filePath: str):
        """
        filepath is the filepath of your txt, csv, or xlsx file relative to this directory in str.
        """

        checkType([(filePath, str)])

        self.__filePath = filePath

    def getFilePath(self):
        """
        Returns the current file path
        """

        return self.__filePath

    def getInput(self):
        """
        Input Format:

        1) The inputs to the Moore Machine can be from files that have the extension .txt, .csv, or .xlsx.
        2) The first line of each file should be an header line which can contain anything, the program will automatically skip it / ignore it.
        3) The second line of each file should contain the number of bits for each input field. The first value for the time can be anything (it would be ignored). If the inputs given contain more number of bits than specified, then an error would be thrown.
        4) The next how many ever lines should be the inputs.
        5) If there are any empty elements, an error would be thrown.
        Example on how to generate a csv file:
        
        import csv
        with open("Test.csv", "w", newline='') as file:
            csw=csv.writer(file)
            csw.writerow['-',3]
            for i in range(5):
                csw.writerow([i+0.1,i+1])
        Sample Input Format:
        
        Txt File:
        
        Time Input1 Input2 Input3
        --- 3 3 3
        0.1 1 2 0
        1.1 2 4 5
        2.1 3 5 2
        3.1 4 5 0
        4.1 5 0 0
        CSV File:
        
        time,input1,input2,input3
        ---,3,3,3
        0.1,1,2,0
        1.1,2,4,5
        2.1,3,5,2
        3.1,4,5,0
        4.1,5,0,0
        XLSX File:
        
        Column: A    B      C      D
                Time Input1 Input2 Input3
                -    3      3      3
                0.1  1      2      0
                1.1  2      4      5
                2.1  3      5      2
                3.1  4      5      0
                4.1  5      0      0
        Internally, all the inputs would be combined into one input wire. For example, the generated input from the above input would be:
        
        Generated Input:
        
            Time Input
            0.1  ("001" + "010" + "000") = "001010000" = 80
            1.1  ("010" + "100" + "101") = "010100101" = 165
            2.1  ("011" + "101" + "010") = "011101010" = 234
            3.1  ("100" + "101" + "000") = "100101000" = 296
            4.1  ("101" + "000" + "000") = "101000000" = 320
        Thus, all the above formats shown generate the same input of [80, 165, 234, 296, 320] at times [0.1, 1.1, 2.1, 3.1, 4.1] respectively.
        """

        try:
            if (self.__filePath.endswith(".csv")):
                return self.__openCsvFile()
            elif (self.__filePath.endswith(".txt")):
                return self.__openTxtFile()
            elif (self.__filePath.endswith(".xlsx")):
                return self.__openExcelFile()
            else:
                raise ValueError("File path is not of type csv, txt, or xlsx.")

        except ValueError as e:
            printErrorAndExit(e)

    def __openCsvFile(self):
        """
        Returns valid input from a csv file
        """

        import csv
        try:
            with open(self.__filePath, "r", newline='') as file:
                csr = csv.reader(file)
                return self.__returnProperInputs(csr)
        except IOError:
            printErrorAndExit(f"The file path {self.__filePath} does not exist.")
        except ValueError as e:
            printErrorAndExit(e)

    def __openTxtFile(self):
        """
        Returns valid input from a txt file
        """

        try:
            with open(self.__filePath, 'r') as fh:
                lines = fh.readlines()
                lines = list(map(lambda x: x.split(" "), lines))
                return self.__returnProperInputs(lines)
        except IOError:
            printErrorAndExit(f"The file path {self.__filePath} does not exist.")
        except ValueError as e:
            printErrorAndExit(e)

    def __openExcelFile(self):
        """
        Returns valid input from an excel file
        """

        import openpyxl as xl

        try:
            wb = xl.load_workbook(self.__filePath)
            sheet = wb.active
            return self.__returnProperInputs(sheet.values)
        except IOError:
            printErrorAndExit(f"The file path {self.__filePath} does not exist.")
        except ValueError as e:
            printErrorAndExit(e)

    def __returnProperInputs(self, iterable):
        """
        This function return the input_schedule in form a dictionary.
        The output format is
            {\"Inputs\": [(time1, input1), (time2, input2), ...]}
        This function expects an iterable object.
        This function raises a ValueError if any error is encountered. 
        """

        def to_binary(val):
            return bin(int(val))[2:]

        def to_decimal(val):
            return int(val, 2)
        
        def pad_with_zeros(value):

            if(len(value) > length):
                printErrorAndExit("Number of bits in input is bigger than that specified by the first column.")
            
            padded_value = str(value).zfill(length)
            return padded_value

        #For txt files
        df = pd.DataFrame(data = iterable).replace("\n", "", regex = True)

        if df.isnull().values.any():
            printErrorAndExit("Input contains illegal values.")

        df.columns = df.iloc[0]
        df = df.drop(df.index[0])
        
        try:
            df.set_index(df.columns[0], inplace = True)
            df = df.astype(int)
            df = df.astype(str)
            df.iloc[1:,:] = df.iloc[1:,:].apply(lambda x: x.apply(to_binary))            
        except ValueError as e:
            printErrorAndExit("Input contains illegal values.")

        for col in df.columns:
            length = int(df[col].iloc[0])

            df[col].iloc[1:] = df[col].iloc[1:].apply(pad_with_zeros)

        df = df.drop(df.index[0])
        df['Input'] = df.apply(lambda row: ''.join(map(str, row)), axis=1)
        df.drop(df.columns.difference(['Input']), axis=1, inplace=True)
        df.reset_index(inplace = True)
        
        try:
            df[df.columns[0]] = df[df.columns[0]].astype(float)
            df[df.columns[1]] = df[df.columns[1]].apply(to_decimal).astype(int)
        except ValueError as e:
            printErrorAndExit("Input contains illegal values.")

        list_of_tuples = [tuple([float(x[0]), int(x[1])]) for x in df.to_records(index=False)]
        
        return {"Inputs":list_of_tuples}

if __name__ == "__main__":

    # Correct ways for getting inputs
    # Note: Test.txt, Test.csv and Test.xlsx must be in the same directory
    fileInput = InputGenerator("Tests\\Test.txt")
    inputs = fileInput.getInput()
    print(inputs)

    fileInput.setFilePath("Tests\\Test.xlsx")
    inputs = fileInput.getInput()
    print(inputs)

    fileInput.setFilePath("Tests\\Test.csv")
    inputs = fileInput.getInput()
    print(inputs)

    print("Current File Path", fileInput.getFilePath())
    print("String Representation:", fileInput)

    # Incorrect ways for getting inputs
    # It generates error message and exits

    # fileInput.setFilePath("Test1.txt")
    # inputs = fileInput.getInput()
    # print(inputs)

    # fileInput.setFilePath("Test1.xlsx")
    # inputs = fileInput.getInput()
    # print(inputs)

    # fileInput.setFilePath("Test1.csv")
    # inputs = fileInput.getInput()
    # print(inputs)

    # fileInput.setFilePath(2)
    # inputs = fileInput.getInput()
    # print(inputs)

    # fileInput.setFilePath(None)
    # inputs = fileInput.getInput()
    # print(inputs)

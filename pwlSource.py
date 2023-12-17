"""
This class is used for getting input from the user.
The valid formats are txt, csv, and xlsx.
In order to use this class for reading xlsx, one needs to have openpyxl installed.
One can install openpyxl by the following method:
    pip install openpyxl

@author: Abhirath, Aryan, Gathik
@date: 13/12/2023
@version: 1.0
"""

import sys

class InputGenerator:

    def __init__(self, filePath:str):
        """
        filepath is the filepath of your txt, csv, or xlsx file relative to this directory in str.
        """

        self.setFilePath(filePath)

    def __str__(self):
        """
        returns the linked file name
        """
        
        return f"The file linked is: {self.getFilePath()}"
    
    def setFilePath(self, filePath:str):
        """
        filepath is the filepath of your txt, csv, or xlsx file relative to this directory in str.
        """
        
        try:
            if(filePath == None or not isinstance(filePath, str)):
                raise TypeError(f"File path \"{filePath}\" is not of type string.")

            self.__filePath = filePath

        except TypeError as e:
            self.__printErrorAndExit(e)
    
    def getFilePath(self):
        """
        Returns the current file path
        """

        return self.__filePath
    
    def getInput(self):
        """
        This function reads the input stored in the file specified by the given filePath.
        For txt files, the delimiter should be a space ' '
        For csv files, the delimiter should be a comma ','
        For xlsx files, the columns used should be A and B

        Feature: Each of the specified file types can have a header line which can contain anything,
                 the program will automatically skip it / ignore it.
        
        For txt files, the format should be as follows: 
            Input format that is expected in the file as follows:
            <time> <input>
            <time> <input>
            ...


            time should be convertible to float.
            input should be convertible to integer
        
        For csv files, the format should be as follows:
            This function reads inputs from a csv file.
            It assumes that the newline was set to "" while creating the file 

            A sample creation in python:
            
                import csv
                with open("Test.csv", "w", newline='') as file:
                    csw=csv.writer(file)
                    for i in range(5):
                        csw.writerow([i+0.1,i+1])

            Input format that is expected in the file as follows:
            <time>,<input>
            <time>,<input>
            ...

            time should be convertible to float.
            input should be convertible to integer

        For xlsx files, the format should be as follows:
            Input format is expected in the file as follows:
            Column:  A         B
                    <time>   <input>
                    <time>   <input>
                    <time>   <input>
                    ...


            time should be convertible to a float
            input should be convertible to integer 

        Returns a list consisting of (time, input) as entries  
        """

        try:
            if(self.__filePath.endswith(".csv")):
                return self.__openCsvFile()
            elif(self.__filePath.endswith(".txt")):
                return self.__openTxtFile()
            elif(self.__filePath.endswith(".xlsx")):
                return self.__openExcelFile()
            else:
                raise ValueError("File path is not of type csv, txt, or xlsx.")
        
        except ValueError as e:
           self.__printErrorAndExit(e)
    
    def __openCsvFile(self):
        """
        Returns valid input from a csv file
        """

        import csv
        try:
            with open(self.__filePath, "r", newline='') as file:
                csr=csv.reader(file)
                return self.__returnProperInputs(csr)
        except IOError:
            self.__printErrorAndExit(f"The file path {self.__filePath} does not exist.")
        except ValueError as e:
            self.__printErrorAndExit(e)
        
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
            self.__printErrorAndExit(f"The file path {self.__filePath} does not exist.")
        except ValueError as e:
            self.__printErrorAndExit(e)

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
            self.__printErrorAndExit(f"The file path {self.__filePath} does not exist.")
        except ValueError as e:
            self.__printErrorAndExit(e)
    
    def __returnProperInputs(self, iterable):
        """
        This function return the input_schedule in form a dictionary.
        The output format is
            {\"Inputs\": [(time1, input1), (time2, input2), ...]}
        This function expects an iterable object.
        This function raises a ValueError if any error is encountered. 
        """

        input_schedule = []
        counter = 0
        try:
            for row in iterable:
                row = [i for i in row if i]
                if(len(row) == 2):
                    try:
                        input_schedule.append((float(row[0]), int(row[1])))
                    except (ValueError, TypeError):
                        if(counter != 0):
                            raise ValueError(f"Input Error: Inputs are not valid type. Check row {counter + 1} of file {self.getFilePath()}.")
                else:   
                    raise ValueError(f"Input Error: Corrupt input/Garbage input because row {counter + 1} is not of length 2. Check file {self.getFilePath()}.")
                counter += 1
        except TypeError:
            raise ValueError(f"{iterable} cannot be iterated upon.")

        return {"Inputs": input_schedule}

    def __printErrorAndExit(self, message:str):
        """
        This function prints the error message specified by message and exits. 
        """

        print(message)
        sys.exit(1)

if __name__ == "__main__":

    #Correct ways for getting inputs
    #Note: Test.txt, Test.csv and Test.xlsx must be in the same directory
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

    #Creating the CSV file
    #import csv
    #with open("Tests\\Test.csv", "w", newline='') as file:
    #    csw=csv.writer(file)
    #    for i in range(5):
    #        csw.writerow([i+0.1,i+1])
    
    #Incorrect ways for getting inputs
    #It generates error message and exits

    #fileInput.setFilePath("Test1.txt")
    #inputs = fileInput.getInput()
    #print(inputs)
    
    #fileInput.setFilePath("Test1.xlsx")
    #inputs = fileInput.getInput()
    #print(inputs)

    #fileInput.setFilePath("Test1.csv")
    #inputs = fileInput.getInput()
    #print(inputs)

    #fileInput.setFilePath(2)
    #inputs = fileInput.getInput()
    #print(inputs)

    #fileInput.setFilePath(None)
    #inputs = fileInput.getInput()
    #print(inputs)
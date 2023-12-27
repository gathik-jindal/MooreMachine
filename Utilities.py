import sys

def checkType(checkList):

    for arg in checkList:
        if(arg[0] == None or not isinstance(arg[0], arg[1])):
            printErrorAndExit(f"{arg[0]} is not of valid type {arg[1]}.")

    return True

def printErrorAndExit(message:str):
        """
        This function prints the error message specified by message and exits. 
        """

        print(message)
        sys.exit(1)
import sys

def checkType(checkList):
    """
    checkList must be a list of the form
    [(arg1, type1), (arg2, type2), (arg3, type3), ..., (argN, typeN)]
    Returns true if all the types specified are correct and none of the
    arguments are None.
    Throws an Error and exits otherwise.
    """

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
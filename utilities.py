"""
This file contains functions that would be useful across a 
majority of all other files.

checkType : checks the type of variables
printErrorAndExit : prints the error message and closes the program
dumpVars : creates a csv file to dump the variables

@author Abhirath, Aryan, Gathik
@date 4/12/2023
@version 1.6
"""


def checkType(checkList: list):
    """
    checkList must be a list of the form
    [(arg1, type1), (arg2, type2), (arg3, type3), ..., (argN, typeN)]
    Returns true if all the types specified are correct and none of the
    arguments are None.
    Throws an Error and exits otherwise.

    TODO: Convert checkList to an *args type.
    """

    for arg in checkList:
        if (arg[0] == None or not isinstance(arg[0], arg[1])):
            printErrorAndExit(f"{arg[0]} is not of valid type {arg[1]}.")

    return True


def printErrorAndExit(message: str):
    """
    This function prints the error message specified by message and exits. 
    """

    print(message)
    import sys

    sys.exit(1)


def dumpVars(dic: dict, name: str = "dumpVars"):
    """
    This functions dumps all the variables in a csv file.
    If the folder is not present then it is created automatically during runtime.
    """

    keysOfDict = list(dic.keys())
    length = len(dic[keysOfDict[0]])

    import csv
    import os

    if not os.path.exists("output"):
        os.makedirs("output")

    with open(f"output\\{name}.csv", "w", newline='') as file:
        csw = csv.writer(file)

        header = keysOfDict[:]
        header.insert(0, 'Time')
        csw.writerow(header)

        for i in range(round(length)):
            row = [dic[key][i][1] for key in keysOfDict]
            row.insert(0, dic[keysOfDict[0]][i][0])
            csw.writerow(row)

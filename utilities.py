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

def fillEmptyTimeSlots(dic:dict):
    """
    This functions makes sure that every element(list) in the dictionary has a value for every time unit.
    """

    keysOfDict = dic.keys()
    for x in keysOfDict:
        timeCounter = 0
        prevVal = 0
        inputs = dic[x]
        index = 0
        time, values = list(map(list, zip(*inputs)))
        
        while (index < len(time)):
            if timeCounter < time[index]:
                time.insert(index, timeCounter)
                values.insert(index, prevVal)

            timeCounter = int(time[index]) + 1
            prevVal = values[index]
            index += 1
        
        dic[x] = [*zip(time, values)]
    
    return dic
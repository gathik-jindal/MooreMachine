import sys

def checkType(checkList):
    """
    checkList must be a list of the form
    [(arg1, type1), (arg2, type2), (arg3, type3), ..., (argN, typeN)]
    Returns true if all the types specified are correct and none of the
    arguments are None.
    Throws an Error and exits otherwise.

    TODO: Convert checkList to an *args type.
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
    maxTime = 0

    for x in keysOfDict:
        time, values = list(map(list, zip(*dic[x])))

        from math import ceil
        time = [ceil(x) for x in time]

        time.append(maxTime)
        maxTime = max(time)

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
        
        while (timeCounter <= maxTime):
            time.insert(index, timeCounter)
            values.insert(index, prevVal)

            timeCounter += 1
            index += 1
        
        dic[x] = [*zip(time, values)]
    
    return dic

def dumpVars(dic:dict):
    """
    This functions dumps all the variables in a csv file.
    If the folder is not present then it is created automatically during runtime.
    If a value changed in a decimal time like 0.6, it is reflected on the 1st second.

    TODO: add funcitonality for having decimal changes for more exact change.
    """

    keysOfDict = dic.keys()
    maxTime = 0

    for x in keysOfDict:
        time, values = list(map(list, zip(*dic[x])))
        time.append(maxTime)
        maxTime = max(time)

    import csv, os

    if not os.path.exists("output"):
        os.makedirs("output")

    with open("output\\dumpVars.csv", "w", newline='') as file:
        csw=csv.writer(file)

        header = list(keysOfDict)
        header.insert(0, 'Time')
        csw.writerow(header)

        for i in range(maxTime):
            row = [dic[key][i][1] for key in keysOfDict]
            row.insert(0, i)
            csw.writerow(row)
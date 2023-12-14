from openpyxl import load_workbook
# VERSION V1


def readInputsFromExcel(filePath, header=False, sheet=0):
    """
    This function reads inputs from a excel file.
    NOTE: This does not support the xlsv file extension.

    Parameters: filePath, (boolean) header (by defualt its False), sheet (by default opens the active worksheet)

    Input format that is expected in the file is as follows:
    <time> <input>
    <time> <input>
    ...


    time should be convertible to float.
    input should be convertible to integer
    """

    try:
        wb = load_workbook(filename=filePath)
    except:
        print("File Error: Error while opening file.")
        return []

    if sheet == 0:
        ws = wb.active
    else:
        try:
            ws = wb[sheet]
        except:
            print("Sheet Error: Sheet name provided is wrong.")
            return []

    input_schedule = []

    try:
        if not header:
            for time, input in ws.rows:
                input_schedule.append((float(time.value), int(input.value)))
        else:
            rows = tuple(ws.rows)
            for x in range(1, len(rows)):
                input_schedule.append(
                    (float(rows[x][0].value), int(rows[x][1].value)))

    except:
        print("Data Error: File could not be read, data might be corrupt.")

    return input_schedule


def readInputsFromTextFile(filePath, delimiter=" "):
    """
    This function reads inputs from a text file and csv file.

    Parameters: filePath, delimeter (default is set to \" \")

    Input format that is expected in the file is as follows:
    <time> <input>
    <time> <input>
    ...


    time should be convertible to float.
    input should be convertible to integer
    """

    try:
        with open(filePath, 'r') as fh:
            lines = fh.readlines()
            input_schedule = []
            for x in lines:
                tu = x.split(delimiter)
                if len(tu) != 2:
                    print("Input Error: Corrupt input / Garbage input", tu)
                    return input_schedule
                try:
                    input_schedule.append((float(tu[0]), int(tu[1])))
                except:
                    print("Input Error: Inputs are not valid type")

    except FileNotFoundError:
        print("File Error: Does not exist")
        return []

    return input_schedule


print(readInputsFromTextFile("file.txt"))

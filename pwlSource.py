import csv
# VERSION V1


def read_inputs(filePath, delimiter=" "):
    """
    This function reads inputs from a text file and csv file.

    Input format that is expected in the file is as follows:
    <time> <input>
    <time> <input>
    ...


    time should be convertible to float.
    input should be convertible to integer
    """

    try:
        with open(filePath, 'r') as fh:
            # readerObject = csv.reader(fh, delimiter=delimiter)
            # input_schedule = []
            # for x in readerObject:
            #     # x = x[0].split(delimiter)
            #     tu = (float(x[0]), int(x[1]))
            #     input_schedule.append(tu)

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


print(read_inputs("file.txt"))

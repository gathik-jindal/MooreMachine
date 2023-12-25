import sys

class Bus:
    def __init__(self, number:int):
        self.__checkType(number, int)

        if(number < 0):
            self.__printErrorAndExit(f"{number} is not greater than or equal to 0.")
        
        self.__binary = bin(number)[2:]
        self.__number = number

    def getNumber(self):
        return self.__number
    
    def getBinary(self):
        return self.__binary
    
    def __str__(self):
        return self.__binary

    def __getitem__(self, sliced):
        try:
            temp = self.__binary[sliced]

            if(temp == None or temp == ''):
                raise IndexError()
            
            return temp
        except IndexError:
            self.__printErrorAndExit(f"{sliced} is not a valid index.")
        except TypeError:
            self.__printErrorAndExit(f"{sliced} is not of valid type.")
        
    def __add__(self, other):
        self.__checkType(other, Bus)
        return bin(self.__number + other.__number)[2:]

    def append(self, other):
        self.__binary = self.__add__(other)
        self.__number = self.__number + other.__number

    def __checkType(self, value, classType):
        try:
            if(value == None or classType == None or not isinstance(value, classType)):
                raise ValueError(f"{value} is not of type {classType}")
        except ValueError as e:
            self.__printErrorAndExit(e)

    def __printErrorAndExit(self, message:str):
        """
        This function prints the error message specified by message and exits. 
        """

        print(message)
        sys.exit(1)

if __name__ == "__main__":
    bus = Bus(22)

    #Invalid Creations
    #bus = Bus(-2)
    #bus = Bus('A')

    print("To String:", bus)
    print("Number representation:", bus.getNumber())
    print("Binary representation:", bus.getBinary())
    print("Indexing at 2:", bus[2])
    print("Indexing at -2:", bus[-2])
    print("Slicing from [2:5]", bus[2:5])

    #Invalid slicing
    #print(bus[2:2])

    bus2 = Bus(33)

    print("Adding", bus, "and", bus2, bus + bus2)
    
    bus.append(bus2)
    print("After appending bus2 to bus, bus is", bus, "while bus2 is", bus2)

    #Invalid adding
    #bus + 3
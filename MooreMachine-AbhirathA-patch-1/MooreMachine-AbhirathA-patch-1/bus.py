"""
This class is used for simulating a bus.
It allows one to get specific inputs from the bus
and also combine two buses. 
"""

from utilities import printErrorAndExit, checkType

class Bus:
    def __init__(self, number:int):
        """
        Number must of type integer and must be non-negative. 
        Number represents the bus value. 
        """

        checkType([(number, int)])

        if(number < 0):
            printErrorAndExit(f"{number} is not greater than or equal to 0.")

        self.__number = number

    def getNumber(self):
        """
        Returns the numeric representation of the bus value.
        """

        return self.__number
    
    def getBinary(self):
        """
        Returns the binary representation of the bus value. 
        """

        return bin(self.getNumber())[2:]
    
    def __str__(self):
        """
        Returns the string representation of this class.
        The returned value is equivalent to calling getBinary().
        """

        return self.getBinary()

    def __getitem__(self, sliced):
        """
        Returns a Bus value after slicing the bus value. 
        Sliced must be a valid sliced object and must consist
        of only integers.
        If the resulting value is an empty string, then error is
        thrown. 
        """

        try:
            temp = self.getBinary()[sliced]

            if(temp == None or temp == ''):
                raise IndexError()
            
            return Bus(int("0b"+temp, 2))

        except IndexError:
            printErrorAndExit(f"{sliced} is not a valid index.")
        except TypeError:
            printErrorAndExit(f"{sliced} is not of valid type.")
        
    def __add__(self, other):
        """
        Returns a Bus value after adding this object and other object.
        other must be of Bus type. 
        """

        checkType([(other, Bus)])
        return Bus(self.__number + other.__number)

    def iadd(self, other):
        """
        Adds this object with the other object and changes this object's input.
        other must be of Bus type. 
        """

        checkType([(other, Bus)])
        self.__number = self.__number + other.__number

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
    
    bus += bus2
    print("After appending bus2 to bus, bus is", bus, "while bus2 is", bus2)

    #Invalid adding
    #bus + 3
"""
Register Tester Module (File-Based Testing)

Each test uses:
- an INPUT CSV file
- an EXPECTED OUTPUT CSV file

The tester function:
1. Creates pydig environment
2. Loads input file using source()
3. Connects input → register
4. Runs simulation
5. Reads expected output file
6. Compares against register dump
"""

import csv
from pydig import pydig



def read_csv_values(path):
    values = []
    with open(path, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if row and row[0].strip().isdigit():
                values.append(int(row[0]))
    return values



def tester(sim, register, clock, input_file, expected_file, until):
    """
    sim: pydig instance
    register: Register block
    clock: Clock block
    input_file: path to CSV input file
    expected_file: path to CSV expected-output file
    until: simulation time
    """

    inp = sim.source(filePath=input_file, plot=False, blockID="TestInput")

    inp.output() > register.input()

    sim.run(until=until)

    expected_values = read_csv_values(expected_file)

    dump = register.getScopeDump()

    register_signal_key = list(dump.keys())[0]
    actual_values = [val for (_, val) in dump[register_signal_key]]
    key = list(dump.keys())[0]
    actual_values = [val for (_, val) in dump[key]]

    if actual_values == expected_values:
        print("PASS:", expected_values)
    else:
        print("FAIL")
        print("Expected:", expected_values)
        print("Got     :", actual_values)
        raise AssertionError("Register output mismatch")



def test_register_basic():
    sim = pydig("reg_basic")

    clk = sim.clock(timePeriod=1, onTime=0.5, blockID="clk_basic")
    reg = sim.register(clock=clk, delay=0, initalValue=0, blockID="reg_basic")

    tester(
        sim,
        reg,
        clk,
        input_file="Tests/register_input1.csv",
        expected_file="Tests/register_expected1.csv",
        until=20
    )


def test_register_with_delay():
    sim = pydig("reg_delay")

    clk = sim.clock(timePeriod=1, onTime=0.5, blockID="clk_delay")
    reg = sim.register(clock=clk, delay=2, initalValue=0, blockID="reg_delay")

    tester(
        sim,
        reg,
        clk,
        input_file="Tests/register_input2.csv",
        expected_file="Tests/register_expected2.csv",
        until=30
    )


def test_register_initial_value():
    sim = pydig("reg_init")

    clk = sim.clock(timePeriod=1, onTime=0.5, blockID="clk_init")
    reg = sim.register(clock=clk, delay=0, initalValue=7, blockID="reg_init")

    tester(
        sim,
        reg,
        clk,
        input_file="Tests/register_input3.csv",
        expected_file="Tests/register_expected3.csv",
        until=20
    )


def test_register_hold_behavior():
    sim = pydig("reg_hold")

    clk = sim.clock(timePeriod=1, onTime=0.5, blockID="clk_hold")
    reg = sim.register(clock=clk, delay=0, initalValue=3, blockID="reg_hold")

    tester(
        sim,
        reg,
        clk,
        input_file="Tests/register_input4.csv",
        expected_file="Tests/register_expected4.csv",
        until=15
    )


def test_register_invalid_config():
    """
    Negative delay or invalid parameters must raise an exception.
    """

    try:
        sim = pydig("reg_invalid")
        clk = sim.clock(timePeriod=1, onTime=0.5, blockID="clk_inv")
        reg = sim.register(clock=clk, delay=-1, initalValue=0, blockID="reg_invalid")

        print("FAIL: Negative delay should raise error")
    except Exception as e:
        print("PASS: Invalid config caught:", e)




if __name__ == "__main__":
    test_register_basic()
    test_register_with_delay()
    test_register_initial_value()
    test_register_hold_behavior()
    test_register_invalid_config()

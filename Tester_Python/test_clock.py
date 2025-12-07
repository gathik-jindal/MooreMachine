"""
Clock Tester Module (File-Based Testing)

This verifies whether the Clock block produces the correct output waveform.
Each test uses:
- An INPUT CSV file   (even if unused, required by project requirements)
- An EXPECTED CSV file containing the correct clock output

The tester() function:
1. Creates a pydig simulator
2. Loads input file with source()
3. Creates the clock under test
4. Connects nothing to clock (it’s autonomous)
5. Runs simulation
6. Reads expected waveform
7. Compares with recorded clock output

"""

import sys
import os

# Add parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

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


def tester(sim, clock, expected_file, until):
    """
    sim: pydig instance
    clock: Clock block
    input_file: CSV file for input (unused but required for framework)
    expected_file: expected clock waveform
    until: time to simulate
    """

    sim.run(until=until)
    
    dump = clock.getScopeDump()
    
    expected_values = read_csv_values(expected_file)

    if not dump:
        print("FAIL: No scope data recorded for clock block.")
        raise AssertionError("No scope data recorded for clock block.")
    key = list(dump.keys())[0]
    actual_values = [val for (_, val) in dump[key]]

    if actual_values == expected_values:
        print("PASS:", expected_values)
    else:
        print("FAIL")
        print("Expected:", expected_values)
        print("Got     :", actual_values)
        raise AssertionError("Clock waveform mismatch")


def test_clock_basic():
    sim = pydig("clock_basic")

    clk = sim.clock(timePeriod=2, onTime=1, blockID="clk_basic")

    tester(
        sim,
        clk,
        expected_file="../Tests/clock_expected1.csv",
        until=20
    )


def test_clock_duty_cycle():
    sim = pydig("clock_duty")

    clk = sim.clock(timePeriod=4, onTime=1, blockID="clk_duty")

    tester(
        sim,
        clk,
        expected_file="../Tests/clock_expected2.csv",
        until=40
    )


def test_clock_fast():
    sim = pydig("clock_fast")

    clk = sim.clock(timePeriod=1, onTime=0.5, blockID="clk_fast")

    tester(
        sim,
        clk,
        expected_file="../Tests/clock_expected3.csv",
        until=20
    )


def test_clock_initial_high():
    sim = pydig("clock_init_high")

    clk = sim.clock(timePeriod=2, onTime=1, initialValue=1, blockID="clk_init_high")

    tester(
        sim,
        clk,
        expected_file="../Tests/clock_expected4.csv",
        until=20
    )


def test_clock_invalid():
    """
    Invalid timePeriod or onTime should throw an error
    """
    try:
        sim = pydig("clock_invalid")
        clk = sim.clock(timePeriod=-2, onTime=1, blockID="clk_invalid")

        print("FAIL: Negative timePeriod should cause an exception")
    except (Exception, SystemExit) as e:
        print("PASS: Invalid clock caught:", e)


if __name__ == "__main__":
    test_clock_basic()
    test_clock_duty_cycle()
    test_clock_fast()
    test_clock_initial_high()
    test_clock_invalid()

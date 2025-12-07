"""
Source Block Tester (File-Based Testing)

This verifies whether the Source block correctly reads external files and
outputs the expected signal sequence.

Each test uses:
- INPUT FILE: the actual file the Source block will read
- EXPECTED FILE: what the Source block *should* output

Tester verifies:
1. pydig creates a Source block from file
2. Source outputs correct values
3. Output is compared to expected CSV file
4. Raises AssertionError on mismatch
"""

import sys
import os

# Add parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

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


def tester(sim, source_block, expected_file, until):
    """
    sim: pydig instance
    source_block: Input block created by sim.source()
    expected_file: file path to expected output CSV
    until: simulation time
    """

    sim.run(until=until)

    expected = read_csv_values(expected_file)

    dump = source_block.getScopeDump()

    if not dump:
        raise ValueError("No scope data available")
    key = list(dump.keys())[0]
    actual = [val for (_, val) in dump[key]]
        
    if actual == expected:
        print(f"PASS: {len(expected)} values matched")
    else:
        print("FAIL")
        print("Expected:", expected)
        print("Got     :", actual)
        raise AssertionError("Source output mismatch")



def test_source_basic():
    """
    Basic test: Source reads small CSV file and outputs values correctly.
    """
    sim = pydig("source_basic")
    src = sim.source("../../Tests/source_input1.csv", plot=False, blockID="src_basic")

    tester(
        sim,
        src,
        expected_file="../../Tests/source_expected1.csv",
        until=20
    )


def test_source_long_file():
    """
    Larger input file to confirm Source handles long sequences.
    """
    sim = pydig("source_long")
    src = sim.source("../../Tests/source_input2.csv", plot=False, blockID="src_long")

    tester(
        sim,
        src,
        expected_file="../../Tests/source_expected2.csv",
        until=40
    )


def test_source_multibit():
    """
    Source file containing values > 1 (e.g., 2-bit or 4-bit inputs encoded as decimals).
    """
    sim = pydig("source_multibit")
    src = sim.source("../../Tests/source_input3.csv", plot=False, blockID="src_multi")

    tester(
        sim,
        src,
        expected_file="../../Tests/source_expected3.csv",
        until=20
    )


def test_source_invalid_file_format():
    """
    Should fail if file is malformed or not readable.
    """
    try:
        sim = pydig("source_invalid")
        src = sim.source("../../Tests/not_a_real_file.csv", plot=False, blockID="src_bad")

        sim.run(until=10)
        print("FAIL: Expected exception due to missing file.")
    except (Exception, SystemExit) as e:
        print("PASS: Invalid file caught:", e)


def test_source_text_format():
    """
    Test using a .txt input file to ensure non-CSV formats work.
    """
    sim = pydig("source_text_test")
    src = sim.source("../../Tests/source_input4.txt", plot=False, blockID="src_txt")

    tester(
        sim,
        src,
        expected_file="../../Tests/source_expected4.csv",
        until=30
    )


if __name__ == "__main__":
    test_source_basic()
    test_source_long_file()
    test_source_multibit()
    test_source_invalid_file_format()
    test_source_text_format()

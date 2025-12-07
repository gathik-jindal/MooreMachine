"""
Output Block Tester (File-Based Testing)

The Output block collects incoming signals and stores them internally.
This tester verifies that the Output block correctly records values
received from upstream blocks.

Each test uses:
- INPUT FILE: the data sent into the Output block (through a Source block
              or a Combinational block)
- EXPECTED FILE: the waveform that Output block should store

The tester:
1. Creates pydig simulator
2. Creates a Source block from input file
3. Feeds its output into Output block
4. Runs simulation
5. Compares Output block's dump with expected CSV file
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



def tester(sim, output_block, input_file, expected_file, until):
    """
    sim : pydig instance
    output_block : Output block created by sim.output()
    input_file : CSV input file whose values will flow into Output block
    expected_file : CSV expected results
    until : simulation time
    """

    src = sim.source(filePath=input_file, plot=False, blockID="OutputTestInput")

    src.output() > output_block.input()

    sim.run(until=until)

    expected = read_csv_values(expected_file)

    dump = output_block.getScopeDump()
    if not dump:
        print("FAIL")
        print("Expected:", expected)
        print("Got     : <no output>")
        raise AssertionError("Output block produced no output")
    key = list(dump.keys())[0]
    actual = [val for (_, val) in dump[key]]

    if actual == expected:
        print("PASS:", expected)
    else:
        print("FAIL")
        print("Expected:", expected)
        print("Got     :", actual)
        raise AssertionError("Output block mismatch")



def test_output_basic(input_file, expected_file):
    """Simple pass-through test."""
    sim = pydig("output_basic")
    out = sim.output(plot=False, blockID="out_basic")

    tester(
        sim,
        out,
        input_file=input_file,
        expected_file=expected_file,
        until=20
    )


def test_output_empty(input_file, expected_file):
    """
    Output should handle empty or all-zero inputs gracefully.
    """
    sim = pydig("output_empty")
    out = sim.output(plot=False, blockID="out_empty")

    tester(
        sim,
        out,
        input_file,
        expected_file,
        until=10
    )


def test_output_multibit(input_file, expected_file):
    """
    Output must correctly store multi-bit encoded integer signals.
    """
    sim = pydig("output_multibit")
    out = sim.output(plot=False, blockID="out_multibit")

    tester(
        sim,
        out,
        input_file,
        expected_file,
        until=20
    )


def test_output_with_combinational(input_file, expected_file):
    """
    Data flows through a combinational block before reaching output.
    Ensures Output records downstream values, not raw input.
    """
    sim = pydig("output_combi")
    out = sim.output(plot=False, blockID="out_combi")

    src = sim.source(input_file, plot=False, blockID="src4")

    comb = sim.combinational(
        maxOutSize=1,
        plot=False,
        blockID="negate_lsb",
        func=lambda x: (~x) & 0b1
    )

    src.output() > comb.input()
    comb.output() > out.input()

    sim.run(until=20)

    expected = read_csv_values(expected_file)
    dump = out.getScopeDump()
    key = list(dump.keys())[0]
    actual = [val for (_, val) in dump[key]]

    if actual == expected:
        print("PASS:", expected)
    else:
        print("FAIL")
        print("Expected:", expected)
        print("Got     :", actual)
        raise AssertionError("Output combinational mismatch")


def test_output_invalid_connection():
    """
    Output block with no input should raise an error in sim.run().
    """
    try:
        sim = pydig("output_invalid")
        out = sim.output(plot=False, blockID="out_invalid")

        sim.run(until=10)

        print("FAIL: Expected unconnected output to cause an error")
    except (Exception, SystemExit) as e:
        print("PASS: Unconnected output caught:", e)



if __name__ == "__main__":
    test_output_basic()
    test_output_empty()
    test_output_multibit()
    test_output_with_combinational()
    test_output_invalid_connection()

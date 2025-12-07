"""
Combinational Block Tester (File-Based)

A combinational block should:
1. Read inputs from upstream blocks (often a Source block)
2. Apply a user-specified logic function func(x)
3. Output the computed value with optional delay

This tester verifies the correctness of that output
by comparing with an expected CSV waveform.

Each test uses:
- INPUT CSV: values fed into the combinational block
- EXPECTED CSV: correct output values

Tester checks functional correctness.
"""

import csv
from pydig import pydig




def read_csv_values(path):
    values = []
    with open(path, "r") as f:
        for row in csv.reader(f):
            if row and row[0].strip().lstrip("-").isdigit():
                values.append(int(row[0]))
    return values


def tester(sim, combi_block, input_file, expected_file, until):
    """
    sim: pydig instance
    combi_block: Combinational block under test
    input_file: CSV file for input
    expected_file: CSV file for expected output
    until: simulation duration
    """

    src = sim.source(filePath=input_file, plot=False, blockID="CombiInput")

    src.output() > combi_block.input()

    sim.run(until=until)

    expected = read_csv_values(expected_file)

    dump = combi_block.getScopeDump()
    scope_key = list(dump.keys())[0]
    actual = [v for (_, v) in dump[scope_key]]
    key = list(dump.keys())[0]
    actual = [v for (_, v) in dump[key]]

    if actual == expected:
        print("PASS:", expected)
    else:
        print("FAIL")
        # Find first mismatching index
        mismatch_index = None
        for i, (a, e) in enumerate(zip(actual, expected)):
            if a != e:
                mismatch_index = i
                break
        if mismatch_index is None and len(actual) != len(expected):
            mismatch_index = min(len(actual), len(expected))
        if mismatch_index is not None:
            msg = (
                f"Combinational block mismatch at index {mismatch_index}:\n"
                f"  Input file: {input_file}\n"
                f"  Expected file: {expected_file}\n"
                f"  Expected value: {expected[mismatch_index] if mismatch_index < len(expected) else 'N/A'}\n"
                f"  Actual value: {actual[mismatch_index] if mismatch_index < len(actual) else 'N/A'}"
            )
        else:
            msg = (
                f"Combinational block mismatch:\n"
                f"  Input file: {input_file}\n"
                f"  Expected file: {expected_file}\n"
                f"  Lists differ in length: expected {len(expected)}, got {len(actual)}"
            )
        raise AssertionError(msg)
        print("Got     :", actual)
        raise AssertionError("Combinational block mismatch")




def test_combinational_identity():
    """
    Comb(x) = x  (identity function)
    """
    sim = pydig("combi_id")

    comb = sim.combinational(
        maxOutSize=1,
        plot=False,
        blockID="comb_id",
        func=lambda x: x
    )

    tester(
        sim, comb,
        input_file="Tests/combi_input1.csv",
        expected_file="Tests/combi_expected1.csv",
        until=20
    )


def test_combinational_not_gate():
    """
    Comb(x) = NOT(x & 1)
    """
    sim = pydig("combi_not")

    comb = sim.combinational(
        maxOutSize=1,
        plot=False,
        blockID="comb_not",
        func=lambda x: (~x) & 0b1
    )

    tester(
        sim, comb,
        input_file="Tests/combi_input2.csv",
        expected_file="Tests/combi_expected2.csv",
        until=20
    )


def test_combinational_double():
    """
    Comb(x) = x * 2
    """
    sim = pydig("combi_double")

    comb = sim.combinational(
        maxOutSize=1,
        plot=False,
        blockID="comb_double",
        func=lambda x: x * 2
    )

    tester(
        sim, comb,
        input_file="Tests/combi_input3.csv",
        expected_file="Tests/combi_expected3.csv",
        until=20
    )


def test_combinational_chain():
    """
    Test: Source → Comb1 → Comb2 → Output
    The combinational block under test is Comb2.
    """

    sim = pydig("combi_chain")

    src_file = "Tests/combi_input4.csv"

    comb1 = sim.combinational(
        maxOutSize=1,
        blockID="comb_plus1",
        func=lambda x: x + 1
    )

    comb2 = sim.combinational(
        maxOutSize=1,
        blockID="comb_times2",
        func=lambda x: x * 2
    )

    src = sim.source(src_file, blockID="src4")
    src.output() > comb1.input()
    comb1.output() > comb2.input()

    sim.run(until=25)

    expected = read_csv_values("Tests/combi_expected4.csv")
    dump = comb2.getScopeDump()
    key = list(dump.keys())[0]
    actual = [v for (_, v) in dump[key]]

    if actual == expected:
        print("PASS:", expected)
    else:
        print("FAIL")
        print("Expected:", expected)
        print("Got     :", actual)
        raise AssertionError("Combinational chain mismatch")


def test_combinational_invalid():
    """
    Invalid parameter test: func = None or maxOutSize = 0
    Should throw an error.
    """
    try:
        sim = pydig("combi_invalid")

        comb = sim.combinational(
            maxOutSize=0,
            blockID="bad_combi",
            func=lambda x: x
        )
        print("FAIL: Expected error for invalid maxOutSize")
    except Exception as e:
        print("PASS: Invalid configuration caught:", e)



if __name__ == "__main__":
    test_combinational_identity()
    test_combinational_not_gate()
    test_combinational_double()
    test_combinational_chain()
    test_combinational_invalid()

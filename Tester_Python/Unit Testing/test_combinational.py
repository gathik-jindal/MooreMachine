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

import sys
import os

# Add parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import csv
from pydig import pydig
from usableBlocks import Input  # added for combinational wiring tests


def read_csv_values(path):
    values = []
    with open(path, "r") as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        for row in reader:
            if len(row) >= 2:
                try:
                    values.append(int(row[1]))
                except ValueError:
                    pass
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


def register_manual_block(sim, block):
    """
    For tests that directly construct Input or other blocks (not through
    the pydig.* convenience methods), manually register them into the
    pydig instance so sim.run() will call their run() methods.
    """
    sim._pydig__components.append(block)


def get_block_values(block, prefix):
    """
    Extract integer values from a block's ScopeDump where the
    classification key contains the given prefix.

    Returns:
        list[int]: list of values in chronological order.
    """
    dump = block.getScopeDump()
    # Prefer keys starting with prefix; fall back to 'prefix in k'.
    keys = [k for k in dump if k.startswith(prefix)]
    if not keys:
        keys = [k for k in dump if prefix in k]
    if not keys:
        return []

    key = keys[0]
    return [v for (_, v) in dump[key]]


# ---------- 1) basic testing of Combinational ----------

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
        input_file="../../Tests/combi_input1.csv",
        expected_file="../../Tests/combi_expected1.csv",
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
        input_file="../../Tests/combi_input2.csv",
        expected_file="../../Tests/combi_expected2.csv",
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
        input_file="../../Tests/combi_input3.csv",
        expected_file="../../Tests/combi_expected3.csv",
        until=20
    )


def test_combinational_chain():
    """
    Test: Source → Comb1 → Comb2 → Output
    The combinational block under test is Comb2.
    """

    sim = pydig("combi_chain")

    src_file = "../../Tests/combi_input4.csv"

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

    expected = read_csv_values("../../Tests/combi_expected4.csv")
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

        sim.combinational(
            maxOutSize=0,
            blockID="bad_combi",
            func=lambda x: x
        )
        print("FAIL: Expected error for invalid maxOutSize")
    except SystemExit as e:
        print("PASS: Invalid configuration caught:", e)


# ---------- 2) parallel inputs merging into a single Combinational ----------

def test_comb_parallel_inputs_merge():
    """
    Two parallel 2-bit inputs merged into a single 4-bit input of a
    Combinational block.

    Input A: 2-bit values
    Input B: 2-bit values
    Effective packed input = A + (B << 2)

    The combinational block is identity: func(x) = x.
    We verify that its *output* obeys this packing by comparing the
    inputs' traces to the combinational output trace.
    """
    print("Running test_comb_parallel_inputs_merge...")

    sim = pydig("comb_parallel")

    # Two 2-bit input sequences
    inA = Input(
        inputList=[(0.0, 1), (2.0, 2), (4.0, 3)],  # 01, 10, 11
        env=sim.getEnv(),
        blockID="inA",
        plot=False,
    )
    inB = Input(
        inputList=[(0.0, 0), (2.0, 1), (4.0, 2)],  # 00, 01, 10
        env=sim.getEnv(),
        blockID="inB",
        plot=False,
    )
    register_manual_block(sim, inA)
    register_manual_block(sim, inB)

    # Combinational block: identity function on a 4-bit word
    comb = sim.combinational(
        maxOutSize=4,
        plot=False,
        blockID="comb_parallel",
        func=lambda x: x,
        delay=0.0,
    )

    # Connect both inputs into the same combinational input.
    # Each Input contributes 2 bits, so HasInputConnections packing gives:
    #   packed = A + 4 * B
    inA.output() > comb.input()
    inB.output() > comb.input()

    sim.run(until=6)

    # Get values from the two Inputs and from the combinational output
    inA_vals = get_block_values(inA, "Input to")
    inB_vals = get_block_values(inB, "Input to")
    comb_vals = get_block_values(comb, "comb_parallel output")

    # Last 3 values correspond to the 3 scheduled changes
    A_tail = inA_vals[-3:]
    B_tail = inB_vals[-3:]
    C_tail = comb_vals[-3:]

    print("inA last 3:", A_tail)
    print("inB last 3:", B_tail)
    print("comb output last 3:", C_tail)

    ok_merge = all(
        C_tail[i] == A_tail[i] + (B_tail[i] << 2)
        for i in range(3)
    )

    if ok_merge:
        print("PASS: test_comb_parallel_inputs_merge")
    else:
        print("FAIL: test_comb_parallel_inputs_merge")
        raise AssertionError("Combinational parallel input merge failed")


# ---------- 3) Combinational output slicing to multiple Outputs ----------

def test_comb_output_slicing():
    """
    Combinational block has a 4-bit output (0..15).
    We slice the output into:
        low 2 bits  -> Output 'out_low'
        high 2 bits -> Output 'out_high'

    Then we verify that these outputs match the bit-sliced original.
    """
    print("Running test_comb_output_slicing...")

    sim = pydig("comb_slicing")

    # Input: 4-bit values over time
    src_vals = [
        (0.0, 0b0001),
        (1.0, 0b0110),
        (2.0, 0b1011),
        (3.0, 0b1110),
    ]
    src = Input(
        inputList=src_vals,
        env=sim.getEnv(),
        blockID="comb_src",
        plot=False,
    )
    register_manual_block(sim, src)

    # Combinational: identity over 4 bits
    comb = sim.combinational(
        maxOutSize=4,
        blockID="comb_slice",
        func=lambda x: x,
        plot=False,
        delay=0.0,
    )

    src.output() > comb.input()

    out_low = sim.output(plot=False, blockID="out_low")
    out_high = sim.output(plot=False, blockID="out_high")

    # Slice connections:
    #   lower 2 bits (0,2)
    #   upper 2 bits (2,4)
    comb.output(0, 2) > out_low.input()
    comb.output(2, 4) > out_high.input()

    sim.run(until=5)

    full_vals = get_block_values(comb, "comb_slice output")
    low_vals = get_block_values(out_low, "Final Output from")
    high_vals = get_block_values(out_high, "Final Output from")

    print("comb outputs:", full_vals)
    print("low slice:", low_vals)
    print("high slice:", high_vals)

    # Align lengths (in case of extra initial values)
    n = min(len(full_vals), len(low_vals), len(high_vals))
    full_vals = full_vals[-n:]
    low_vals = low_vals[-n:]
    high_vals = high_vals[-n:]

    ok_slicing = all(
        (low_vals[i] == (full_vals[i] & 0b11) and
         high_vals[i] == (full_vals[i] >> 2))
        for i in range(n)
    )

    if ok_slicing:
        print("PASS: test_comb_output_slicing")
    else:
        print("FAIL: test_comb_output_slicing")
        raise AssertionError("Combinational output slicing failed")


# ---------- 4) Combinational running with no func ----------

def test_comb_missing_logic():
    """
    Combinational created without a valid func should be rejected.
    Here we pass func=None and expect a runtime error when the block runs.
    """
    print("Running test_comb_missing_logic...")

    try:
        sim = pydig("comb_missing_logic")

        # Create a combinational block with func=None
        bad = sim.combinational(
            maxOutSize=1,
            blockID="bad_comb",
            func=None,   # missing logic
            plot=False,
        )

        # Provide an input so the block actually executes __runFunc
        src = Input(
            inputList=[(0.0, 0), (1.0, 1)],
            env=sim.getEnv(),
            blockID="src_missing",
            plot=False,
        )
        register_manual_block(sim, src)
        src.output() > bad.input()

        sim.run(until=3)

        # If we got here, no error was raised – that's a failure for this test.
        print("FAIL: Expected combinational with missing func to cause an error")

    except TypeError:
        # __func is None, so __func(self.__value) should raise TypeError
        print("PASS: test_comb_missing_logic")


if __name__ == "__main__":
    test_combinational_identity()
    test_combinational_not_gate()
    test_combinational_double()
    test_combinational_chain()
    test_combinational_invalid()

    test_comb_parallel_inputs_merge()
    test_comb_output_slicing()
    test_comb_missing_logic()

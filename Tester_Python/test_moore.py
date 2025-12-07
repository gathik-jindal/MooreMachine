from pydig import pydig
from usableBlocks import Input, Output  # Input/Output live in usableBlocks.py
import sys


# ---------- small helpers ----------

def get_block_values(block, label_contains):
    """
    Fetch integer values from the block's ScopeDump for the first key
    containing label_contains.
    """
    dump = block.getScopeDump()
    keys = [k for k in dump if label_contains in k]
    if not keys:
        # Fall back to "last key" if label not found
        key = list(dump.keys())[-1]
    else:
        key = keys[0]
    return [v for (_, v) in dump[key]]


def register_manual_block(sim, block):
    """
    pydig keeps its component list private (__components),
    but Python just name-mangles it. This helper registers a
    manually created block (like an Input created directly)
    so that sim.run() will start it.
    """
    sim._pydig__components.append(block)


# ---------- 0) optional basic test ----------

def test_moore_basic():
    """
    Simple mod-2 Moore machine, just as a sanity check.
    """
    print("Running test_moore_basic...")

    sim = pydig("moore_basic")

    # Moore: ps toggles each clock; output = ps
    moore = sim.moore(
        maxOutSize=1,
        blockID="moore_basic",
        startingState=0,
        nsl=lambda ps, i: ps ^ 1,
        ol=lambda ps: ps,
    )

    clk = sim.clock(timePeriod=1.0, onTime=0.5, blockID="clk_basic")
    clk.output() > moore.clock()

    # Dummy input so moore.isConnected() passes, but nsl ignores it
    const_in = Input(inputList=[(0.0, 0)], env=sim.getEnv(),
                     blockID="const_basic", plot=False)
    register_manual_block(sim, const_in)
    const_in.output() > moore.input()

    sim.run(until=5)

    out_vals = get_block_values(moore, "output of")
    print("Moore basic outputs:", out_vals)
    # Should toggle between 0 and 1 at least once
    if len(set(out_vals)) >= 2:
        print("PASS: test_moore_basic")
    else:
        print("FAIL: test_moore_basic")


# ---------- 1) multiple Moores one after the other ----------

def test_moore_cascade():
    """
    Two Moore machines cascaded:
        moore1: 2-bit counter (0->1->2->3->0...)
        moore2: registered copy of moore1's output (one-step delayed)
    """
    print("Running test_moore_cascade...")

    sim = pydig("moore_cascade")

    clk = sim.clock(timePeriod=1.0, onTime=0.5, blockID="clk_cascade")

    # First Moore: 2-bit counter, output = state
    moore1 = sim.moore(
        maxOutSize=2,
        blockID="moore1",
        startingState=0,
        nsl=lambda ps, i: (ps + 1) % 4,
        ol=lambda ps: ps,
        clock=clk,
    )

    # Second Moore: state = input (lower 2 bits), output = state
    moore2 = sim.moore(
        maxOutSize=2,
        blockID="moore2",
        startingState=0,
        nsl=lambda ps, i: i & 0b11,
        ol=lambda ps: ps,
        clock=clk,
    )

    # Dummy constant input for moore1 (nsl ignores it)
    const_in = Input(inputList=[(0.0, 0)], env=sim.getEnv(),
                     blockID="const_cascade", plot=False)
    register_manual_block(sim, const_in)
    const_in.output() > moore1.input()

    # Cascade: moore1 output feeds moore2 input
    moore1.output() > moore2.input()

    sim.run(until=8)

    out1 = get_block_values(moore1, "output of")
    out2 = get_block_values(moore2, "output of")
    print("moore1 outputs:", out1)
    print("moore2 outputs:", out2)

    # Check: moore1 behaves like mod-4 counter
    ok_counter = all(
        out1[i] == (out1[i - 1] + 1) % 4
        for i in range(1, len(out1))
    ) if len(out1) > 1 else False

    # Check: moore2 output is essentially moore1 delayed by one step
    # (ignore first element for simplicity)
    min_len = min(len(out1) - 1, len(out2))
    ok_delay = min_len > 0 and all(
        out2[i] == out1[i]
        for i in range(min_len)
    )

    if ok_counter and ok_delay:
        print("PASS: test_moore_cascade")
    else:
        print("FAIL: test_moore_cascade")


# ---------- 2) parallel inputs merging into a single Moore ----------

def test_moore_parallel_inputs_merge():
    """
    Two parallel 2-bit inputs merged into a single 4-bit input of the Moore machine.

    Input A: 2-bit values
    Input B: 2-bit values
    Moore input = A + (B << 2)

    We verify that 'Input to moore_parallel' obeys this packing
    by comparing against the Input blocks' traces.
    """
    print("Running test_moore_parallel_inputs_merge...")

    sim = pydig("moore_parallel")

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

    clk = sim.clock(timePeriod=1.0, onTime=0.5, blockID="clk_parallel")

    # Moore: next state = input, output = state
    moore = sim.moore(
        maxOutSize=4,
        blockID="moore_parallel",
        startingState=0,
        nsl=lambda ps, i: i,
        ol=lambda ps: ps,
        clock=clk,
    )

    # Connect both inputs into the same Moore input
    # Each Input has maxOutSize=2, so effective packing is:
    #   input_val = A + 4*B
    inA.output() > moore.input()
    inB.output() > moore.input()

    sim.run(until=6)

    # Get values from the two Inputs and from "Input to moore_parallel"
    inA_vals = get_block_values(inA, "Input to")
    inB_vals = get_block_values(inB, "Input to")
    moore_in_vals = get_block_values(moore, "Input to")

    # Last 3 values correspond to the 3 scheduled changes
    A_tail = inA_vals[-3:]
    B_tail = inB_vals[-3:]
    M_tail = moore_in_vals[-3:]

    print("inA last 3:", A_tail)
    print("inB last 3:", B_tail)
    print("moore input last 3:", M_tail)

    ok_merge = all(
        M_tail[i] == A_tail[i] + (B_tail[i] << 2)
        for i in range(3)
    )

    if ok_merge:
        print("PASS: test_moore_parallel_inputs_merge")
    else:
        print("FAIL: test_moore_parallel_inputs_merge")


# ---------- 3) Moore output slicing to multiple Outputs ----------

def test_moore_output_slicing():
    """
    Moore has a 4-bit output (0..15).
    We slice the output into:
        low 2 bits  -> Output 'out_low'
        high 2 bits -> Output 'out_high'

    Then we verify that these outputs match the bit-sliced original.
    """
    print("Running test_moore_output_slicing...")

    sim = pydig("moore_slicing")

    clk = sim.clock(timePeriod=1.0, onTime=0.5, blockID="clk_slicing")

    # Moore: 4-bit counter, output = state
    moore = sim.moore(
        maxOutSize=4,
        blockID="moore_slice",
        startingState=0,
        nsl=lambda ps, i: (ps + 1) & 0b1111,
        ol=lambda ps: ps,
        clock=clk,
    )

    # Dummy constant input; nsl ignores it
    const_in = Input(inputList=[(0.0, 0)], env=sim.getEnv(),
                     blockID="const_slice", plot=False)
    register_manual_block(sim, const_in)
    const_in.output() > moore.input()

    out_low = sim.output(plot=False, blockID="out_low")
    out_high = sim.output(plot=False, blockID="out_high")

    # Slice connections:
    #   lower 2 bits (0,2)
    #   upper 2 bits (2,4)
    moore.output(0, 2) > out_low.input()
    moore.output(2, 4) > out_high.input()

    sim.run(until=8)

    full_vals = get_block_values(moore, "output of")
    low_vals = get_block_values(out_low, "Final Output from")
    high_vals = get_block_values(out_high, "Final Output from")

    print("moore outputs:", full_vals)
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
        print("PASS: test_moore_output_slicing")
    else:
        print("FAIL: test_moore_output_slicing")


# ---------- 4) Moore running with no NSL or OL ----------

def test_moore_missing_logic():
    """
    Moore created without nsl/ol should be rejected.
    isConnected() requires nsl != None and ol != None, so pydig.run()
    should cause a fatal error (SystemExit via printErrorAndExit).
    """
    print("Running test_moore_missing_logic...")

    try:
        sim = pydig("moore_missing_logic")

        clk = sim.clock(timePeriod=1.0, onTime=0.5, blockID="clk_missing")

        bad = sim.moore(
            maxOutSize=1,
            blockID="bad_moore",
            startingState=0,
            nsl=None,      # missing
            ol=None,       # missing
            clock=clk,
        )

        # Provide an input so the only reason to fail is the missing nsl/ol
        const_in = Input(inputList=[(0.0, 0)], env=sim.getEnv(),
                         blockID="const_missing", plot=False)
        register_manual_block(sim, const_in)
        const_in.output() > bad.input()

        sim.run(until=5)
        print("FAIL: Expected moore with missing logic to cause an error")

    except SystemExit:
        print("PASS: test_moore_missing_logic")


if __name__ == "__main__":
    # Call whatever subset you want
    test_moore_basic()
    test_moore_cascade()
    test_moore_parallel_inputs_merge()
    test_moore_output_slicing()
    test_moore_missing_logic()

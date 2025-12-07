from pydig import pydig
from usableBlocks import Input, Output
import sys


# ---------- small helpers ----------

def get_block_values(block, label_contains):
    """
    Fetch integer values from the block's ScopeDump for the first key
    containing `label_contains`.
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
    Register a manually constructed block (like Input created directly)
    into the pydig simulation so that sim.run() will run it.

    pydig stores components in a private attribute __components,
    which Python name-mangles to _pydig__components.
    """
    sim._pydig__components.append(block)


# ---------- 0) basic Mealy test ----------

def test_mealy_basic():
    """
    Basic Mealy: output = input (ol ignores state).
    We verify that the Mealy output eventually matches the Mealy input trace.
    """
    print("Running test_mealy_basic...")

    sim = pydig("mealy_basic")

    # Input that changes over time
    src = Input(
        inputList=[(0.0, 0), (2.0, 1), (4.0, 3), (6.0, 2)],
        env=sim.getEnv(),
        blockID="src_basic",
        plot=False,
    )
    register_manual_block(sim, src)

    clk = sim.clock(timePeriod=1.0, onTime=0.5, blockID="clk_basic")

    # Mealy: state is unused; output = current input
    mealy = sim.mealy(
        maxOutSize=2,
        blockID="mealy_basic",
        startingState=0,
        nsl=lambda ps, i: ps,      # do nothing with state
        ol=lambda ps, i: i,        # purely combinational: output = input
    )

    # Hook up input and clock
    src.output() > mealy.input()
    clk.output() > mealy.clock()

    sim.run(until=8)

    in_vals = get_block_values(mealy, "Input to")
    out_vals = get_block_values(mealy, "output of")

    print("Mealy basic input: ", in_vals)
    print("Mealy basic output:", out_vals)

    # Align lengths from the tail (to avoid initial zeros & scheduling quirks)
    n = min(len(in_vals), len(out_vals))
    in_tail = in_vals[-n:]
    out_tail = out_vals[-n:]

    if in_tail == out_tail:
        print("PASS: test_mealy_basic")
    else:
        print("FAIL: test_mealy_basic")
        print("Aligned input: ", in_tail)
        print("Aligned output:", out_tail)


# ---------- 1) multiple Mealy one after the other (cascade) ----------

def test_mealy_cascade():
    """
    Two Mealy machines cascaded:

        src --> mealy1 --> mealy2

    Both machines implement: output = input (state unused).
    So mealy2's output should match mealy1's output.
    """
    print("Running test_mealy_cascade...")

    sim = pydig("mealy_cascade")

    src = Input(
        inputList=[(0.0, 0), (2.0, 1), (4.0, 3), (6.0, 2)],
        env=sim.getEnv(),
        blockID="src_cascade",
        plot=False,
    )
    register_manual_block(sim, src)

    clk = sim.clock(timePeriod=1.0, onTime=0.5, blockID="clk_cascade")

    mealy1 = sim.mealy(
        maxOutSize=2,
        blockID="mealy1",
        startingState=0,
        nsl=lambda ps, i: ps,
        ol=lambda ps, i: i,
    )

    mealy2 = sim.mealy(
        maxOutSize=2,
        blockID="mealy2",
        startingState=0,
        nsl=lambda ps, i: ps,
        ol=lambda ps, i: i,
    )

    src.output() > mealy1.input()
    mealy1.output() > mealy2.input()

    clk.output() > mealy1.clock()
    clk.output() > mealy2.clock()

    sim.run(until=8)

    out1 = get_block_values(mealy1, "output of")
    out2 = get_block_values(mealy2, "output of")

    print("mealy1 outputs:", out1)
    print("mealy2 outputs:", out2)

    n = min(len(out1), len(out2))
    tail1 = out1[-n:]
    tail2 = out2[-n:]

    if tail1 == tail2 and n > 0:
        print("PASS: test_mealy_cascade")
    else:
        print("FAIL: test_mealy_cascade")
        print("Aligned mealy1:", tail1)
        print("Aligned mealy2:", tail2)


# ---------- 2) parallel inputs merging into a single Mealy ----------

def test_mealy_parallel_inputs_merge():
    """
    Two 2-bit input streams merged into a single 4-bit Mealy input.

        inA: 2-bit
        inB: 2-bit

    Mealy input = inA + (inB << 2)
    Mealy output = input (ol ignores state).

    We verify that the Mealy input trace matches the packed combination of inA and inB.
    """
    print("Running test_mealy_parallel_inputs_merge...")

    sim = pydig("mealy_parallel")

    inA = Input(
        inputList=[(0.0, 1), (2.0, 2), (4.0, 3)],  # 01, 10, 11
        env=sim.getEnv(),
        blockID="inA_mealy",
        plot=False,
    )
    inB = Input(
        inputList=[(0.0, 0), (2.0, 1), (4.0, 2)],  # 00, 01, 10
        env=sim.getEnv(),
        blockID="inB_mealy",
        plot=False,
    )
    register_manual_block(sim, inA)
    register_manual_block(sim, inB)

    clk = sim.clock(timePeriod=1.0, onTime=0.5, blockID="clk_parallel_mealy")

    mealy = sim.mealy(
        maxOutSize=4,
        blockID="mealy_parallel",
        startingState=0,
        nsl=lambda ps, i: ps,
        ol=lambda ps, i: i,  # output = full merged input
    )

    inA.output() > mealy.input()
    inB.output() > mealy.input()
    clk.output() > mealy.clock()

    sim.run(until=6)

    inA_vals = get_block_values(inA, "Input to")
    inB_vals = get_block_values(inB, "Input to")
    mealy_in_vals = get_block_values(mealy, "Input to")
    mealy_out_vals = get_block_values(mealy, "output of")

    print("inA trace:", inA_vals)
    print("inB trace:", inB_vals)
    print("mealy input trace:", mealy_in_vals)
    print("mealy output trace:", mealy_out_vals)

    # Consider only the last 3 changes (our programmed events)
    A_tail = inA_vals[-3:]
    B_tail = inB_vals[-3:]
    M_tail = mealy_in_vals[-3:]
    O_tail = mealy_out_vals[-3:]

    ok_merge = all(
        M_tail[i] == A_tail[i] + (B_tail[i] << 2)
        for i in range(3)
    )
    ok_output = (M_tail == O_tail)

    if ok_merge and ok_output:
        print("PASS: test_mealy_parallel_inputs_merge")
    else:
        print("FAIL: test_mealy_parallel_inputs_merge")
        print("Expected merged:", [A_tail[i] + (B_tail[i] << 2) for i in range(3)])
        print("Actual   input:", M_tail)
        print("Actual  output:", O_tail)


# ---------- 3) Mealy output slicing to multiple Outputs ----------

def test_mealy_output_slicing():
    """
    Mealy has a 4-bit output which simply echoes its 4-bit input.

    We slice the Mealy output as:
        low  2 bits -> out_low
        high 2 bits -> out_high

    and verify that the Outputs see the sliced values correctly.
    """
    print("Running test_mealy_output_slicing...")

    sim = pydig("mealy_slicing")

    clk = sim.clock(timePeriod=1.0, onTime=0.5, blockID="clk_mealy_slice")

    # 4-bit input values over time
    src = Input(
        inputList=[(0.0, 0b0001), (2.0, 0b1010), (4.0, 0b1111)],
        env=sim.getEnv(),
        blockID="src_mealy_slice",
        plot=False,
    )
    register_manual_block(sim, src)

    mealy = sim.mealy(
        maxOutSize=4,
        blockID="mealy_slice",
        startingState=0,
        nsl=lambda ps, i: ps,
        ol=lambda ps, i: i,  # output = input
    )

    src.output() > mealy.input()
    clk.output() > mealy.clock()

    out_low = sim.output(plot=False, blockID="out_low_mealy")
    out_high = sim.output(plot=False, blockID="out_high_mealy")

    # Slices: [0,2) and [2,4)
    mealy.output(0, 2) > out_low.input()
    mealy.output(2, 4) > out_high.input()

    sim.run(until=6)

    full_vals = get_block_values(mealy, "output of")
    low_vals = get_block_values(out_low, "Final Output from")
    high_vals = get_block_values(out_high, "Final Output from")

    print("mealy full outputs:", full_vals)
    print("low slice outputs:", low_vals)
    print("high slice outputs:", high_vals)

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
        print("PASS: test_mealy_output_slicing")
    else:
        print("FAIL: test_mealy_output_slicing")


# ---------- 4) Mealy running with no nsl or ol ----------

def test_mealy_missing_logic():
    """
    Mealy created without nsl/ol should be rejected.

    MealyMachine.isConnected() requires:
        - _clkVal != []
        - nsl != None
        - ol != None
        - isConnectedToInput()

    So with missing nsl/ol, pydig.run() should trigger printErrorAndExit,
    resulting in a SystemExit.
    """
    print("Running test_mealy_missing_logic...")

    try:
        sim = pydig("mealy_missing_logic")

        clk = sim.clock(timePeriod=1.0, onTime=0.5, blockID="clk_missing_mealy")

        bad = sim.mealy(
            maxOutSize=1,
            blockID="bad_mealy",
            startingState=0,
            nsl=None,  # missing
            ol=None,   # missing
        )

        # Make sure it's otherwise "wired correctly":
        src = Input(
            inputList=[(0.0, 0)],
            env=sim.getEnv(),
            blockID="src_missing_mealy",
            plot=False,
        )
        register_manual_block(sim, src)
        src.output() > bad.input()
        clk.output() > bad.clock()

        sim.run(until=5)
        print("FAIL: Expected Mealy with missing logic to cause an error")

    except SystemExit:
        print("PASS: test_mealy_missing_logic")


if __name__ == "__main__":
    test_mealy_basic()
    test_mealy_cascade()
    test_mealy_parallel_inputs_merge()
    test_mealy_output_slicing()
    test_mealy_missing_logic()

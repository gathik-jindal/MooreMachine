"""
Integration test for the PWM example using the pydig simulator.

This test wires up the whole system:

    Source (Tests\\PWM.csv)
        -> Combinational comparators
        -> Moore counter
        -> Clock
        -> Final Output

and then:

    - Runs the full simulation
    - Ensures the CSV dump is generated
    - Checks that the PWM Output signal is non-trivial (changes over time)

We intentionally mirror the example PWM code structure as closely as possible.
"""

import sys
import os

# Add parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import csv
import pydig

# extra imports for latch tests
from pydig import pydig as pd
from usableBlocks import Combinational as Comb, HasOutputConnections as HOC, Clock, Input
from utilities import checkType


# ---------- Logic functions from the PWM example ----------

def n(a):
    # Single-input NOT gate (1-bit)
    return (~a & 0b1)


def nsl_pwm(ps, i):
    """
    Next State Logic for the modulo-4 counter used inside the PWM.

    ps : present state (2 bits)
    i  : input (merged signal from comparators)
    """
    a = (ps >> 1) & 1
    b = (ps >> 0) & 1

    d = (n(a) & b & n(i)) | (a & n(b) & n(i))
    e = (n(b) & n(i))

    return (d << 1) | e


def ol_pwm(ps):
    """
    Output logic for the counter: directly output the state.
    """
    return ps


# ---------- Helper to read the generated CSV ----------

def read_csv_headers_and_first_rows(path):
    """
    Reads the header and the first few rows of a CSV file.

    Returns:
        (header: list[str], rows: list[list[str]])
    """
    with open(path, "r", newline="") as f:
        reader = csv.reader(f)
        rows = list(reader)
    if not rows:
        return [], []
    header = rows[0]
    data_rows = rows[1:]
    return header, data_rows


# ---------- Small helpers for timing tests ----------

def get_series(block, prefix):
    """
    Return the (time, value) series from a block's ScopeDump where
    the key contains `prefix`.
    """
    dump = block.getScopeDump()
    keys = [k for k in dump if prefix in k]
    if not keys:
        return []
    return dump[keys[0]]


def value_at(series, t):
    """
    Given a list of (time, value) sorted by time, return the last value
    at or before time t. Returns None if no sample exists yet.
    """
    last = None
    for (tm, val) in series:
        if tm <= t:
            last = val
        else:
            break
    return last

# ---------- Integration PWM test ----------

def integration_testing_pwm():
    print("Running integration_testing_pwm...")

    # --- Set up simulator (pydig object) ---
    pysim = pydig.pydig(name="PWM")

    # --- Source from file ---
    PWM_Path = "../../Tests/PWM.csv"
    if not os.path.exists(PWM_Path):
        print(f"FAIL: Input file {PWM_Path} not found. "
              "Make sure Tests/PWM.csv exists.")
        return

    PWM_Input = pysim.source(filePath=PWM_Path, plot=False, blockID="PWM Input")

    # --- Clock ---
    clk = pysim.clock(plot=False, blockID="clk", timePeriod=1, onTime=0.5)

    # --- Moore machine (mod-4 counter) ---
    mod4Counter = pysim.moore(
        maxOutSize=2,
        plot=True,
        blockID="Mod 4 Counter",
        startingState=0
    )
    # Attach the logic functions
    mod4Counter.nsl = nsl_pwm
    mod4Counter.ol = ol_pwm

    # --- Comparators ---
    syncResetComparator = pysim.combinational(
        maxOutSize=1,
        plot=False,
        blockID="Sync Reset Comparator",
        func=lambda x: int((x & 3) == (x >> 2)),
        delay=0,
    )

    outputComparator = pysim.combinational(
        maxOutSize=1,
        plot=False,
        blockID="Output Comparator",
        func=lambda x: int((x & 3) > (x >> 2)),
        delay=0,
    )

    # --- Final output ---
    finalOutput = pysim.output(plot=True, blockID="PWM Output")

    # --- Connections (same as example) ---

    # Sync-reset comparator feeds counter input
    syncResetComparator.output() > mod4Counter.input()

    # Clock feeds counter clock input
    clk.output() > mod4Counter.clock()

    # Lower 2 bits of PWM input -> output comparator
    PWM_Input.output(0, 2) > outputComparator.input()
    mod4Counter.output() > outputComparator.input()

    # Upper 2 bits of PWM input -> sync reset comparator
    PWM_Input.output(2, 4) > syncResetComparator.input()
    mod4Counter.output() > syncResetComparator.input()

    # Comparator output -> final output
    outputComparator.output() > finalOutput.input()

    # --- CSV dump + run ---
    pysim.generateCSV()
    pysim.run(until=40)

    # --- Check that CSV was generated ---
    out_csv_path = os.path.join("output", "PWM.csv")
    if not os.path.exists(out_csv_path):
        print(f"FAIL: Expected CSV dump at {out_csv_path} was not created.")
        return

    header, rows = read_csv_headers_and_first_rows(out_csv_path)
    print("Generated CSV header:", header)
    print("First few rows:", rows[:3])

    if "Final Output from PWM Output" not in header:
        print("FAIL: 'Final Output from PWM Output' column not found in generated CSV.")
        return

    # --- Check that PWM Output actually changes over time ---
    idx = header.index("Final Output from PWM Output")
    pwm_values = []
    for row in rows:
        if len(row) > idx:
            try:
                pwm_values.append(int(row[idx]))
            except ValueError:
                pass

    if len(pwm_values) < 2:
        print("FAIL: Not enough PWM Output samples to consider the test meaningful.")
        return

    if len(set(pwm_values)) == 1:
        print("FAIL: PWM Output appears constant (no variation).")
        print("PWM Output values:", pwm_values)
        return

    print("PASS: integration_testing_pwm")


# ---------- Malformed integration test ----------

def integration_testing_pwm_malformed():
    """
    Integration test that *intentionally* mis-connects the PWM design.

    We leave one of the required blocks not fully connected so that
    pydig.run() calls printErrorAndExit("<block> is not connected."),
    which raises SystemExit.

    The test PASSES if SystemExit is raised, and FAILS otherwise.
    """
    print("Running integration_testing_pwm_malformed...")

    PWM_Path = "..\\..\\Tests\\PWM.csv"
    if not os.path.exists(PWM_Path):
        print(f"FAIL: Input file {PWM_Path} not found. "
              "Make sure Tests\\PWM.csv exists.")
        return

    try:
        # --- Set up simulator ---
        pysim = pydig.pydig(name="PWM_malformed")

        # --- Source, clock, counter as usual ---
        PWM_Input = pysim.source(filePath=PWM_Path, plot=False, blockID="PWM Input")
        clk = pysim.clock(plot=False, blockID="clk", timePeriod=1, onTime=0.5)

        mod4Counter = pysim.moore(
            maxOutSize=2,
            plot=False,
            blockID="Mod 4 Counter",
            startingState=0
        )
        mod4Counter.nsl = nsl_pwm
        mod4Counter.ol = ol_pwm

        # --- Comparators ---
        syncResetComparator = pysim.combinational(
            maxOutSize=1,
            plot=False,
            blockID="Sync Reset Comparator",
            func=lambda x: int((x & 3) == (x >> 2)),
            delay=0,
        )

        outputComparator = pysim.combinational(
            maxOutSize=1,
            plot=False,
            blockID="Output Comparator",
            func=lambda x: int((x & 3) > (x >> 2)),
            delay=0,
        )

        finalOutput = pysim.output(plot=False, blockID="PWM Output")

        # --- MALFORMED CONNECTIONS ---

        # 1) We DO connect the output comparator and final output like before:
        outputComparator.output() > finalOutput.input()

        # 2) We connect *only one* input into outputComparator (missing input from mod4Counter)
        PWM_Input.output(0, 2) > outputComparator.input()

        # 3) We create syncResetComparator but NEVER connect *any* inputs to it.
        #    This means syncResetComparator.isConnected() == False.

        # 4) We ALSO forget to connect the clock to the counter:
        #    (no clk.output() > mod4Counter.clock())
        #    So mod4Counter.isConnected() will also be False.
        #
        #    Either of these will cause pydig.run() to call printErrorAndExit()
        #    when it reaches the first unconnected block in its list.

        # --- Run without generateCSV (we just care about the error) ---
        pysim.run(until=10)

        # If we get here, no SystemExit was raised -> FAIL
        print("FAIL: Expected malformed connections to trigger printErrorAndExit/SystemExit")

    except SystemExit:
        # This is the behavior we expect from malformed connections
        print("PASS: integration_testing_pwm_malformed (caught SystemExit due to malformed wiring)")

if __name__ == "__main__":
    integration_testing_pwm()
    print("\n" + "=" * 60 + "\n")
    integration_testing_pwm_malformed() 

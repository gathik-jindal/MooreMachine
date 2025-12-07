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

import os
import csv
import pydig


# ---------- Logic functions from the example ----------

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

def read_csv_headers_and_first_rows(path, max_rows=5):
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
    data_rows = rows[1:max_rows+1]
    return header, data_rows


# ---------- Integration test ----------

def integration_testing_pwm():
    print("Running integration_testing_pwm...")

    # --- Set up simulator (pydig object) ---
    pysim = pydig.pydig(name="PWM")

    # --- Source from file ---
    PWM_Path = "Tests\\PWM.csv"
    if not os.path.exists(PWM_Path):
        print(f"FAIL: Input file {PWM_Path} not found. "
              "Make sure Tests\\PWM.csv exists.")
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

    if "PWM Output" not in header:
        print("FAIL: 'PWM Output' column not found in generated CSV.")
        return

    # --- Check that PWM Output actually changes over time ---
    # Find the column index for PWM Output
    idx = header.index("PWM Output")

    pwm_values = []
    for row in rows:
        if len(row) > idx:
            try:
                pwm_values.append(int(row[idx]))
            except ValueError:
                # Non-integer in the column; ignore for this simple sanity check
                pass

    if len(pwm_values) < 2:
        print("FAIL: Not enough PWM Output samples to consider the test meaningful.")
        return

    if len(set(pwm_values)) == 1:
        print("FAIL: PWM Output appears constant (no variation).")
        print("PWM Output values:", pwm_values)
        return

    print("PASS: integration_testing_pwm")


if __name__ == "__main__":
    integration_testing_pwm()

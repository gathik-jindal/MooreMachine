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


# ---------- Latch implementations (as specified) ----------

class SRLatch(Comb):
    """
    SR latch implemented with cross-coupled NORs.

    Input SR: 2-bit signal where:
        bit 0 -> R
        bit 1 -> S
    Outputs:
        Q (this Comb instance's output)
        ~Q (via getQNot())
    """
    __counter = 0

    def __init__(self, pydig_obj: pd, SR: HOC, plot: bool = True):
        """
        @param pydig_obj : pydig object
        @param SR : the set and reset signal (HasOutputConnections)
        @param plot : whether to plot this latch or not
        """
        checkType([(pydig_obj, pd), (SR, HOC), (plot, bool)])

        SRLatch.__counter += 1

        super().__init__(
            func=lambda x: x,
            env=pydig_obj.getEnv(),
            blockID=f"Q: SR Latch {SRLatch.__counter}",
            maxOutSize=1,
            delay=0,
            plot=plot,
        )
        o = pydig_obj.combinationalFromObject(self)

        self.__o_not = pydig_obj.combinational(
            maxOutSize=1,
            plot=False,
            blockID=f"~Q: SR Latch {SRLatch.__counter}",
            func=lambda x: x,
            delay=0,
        )

        # Cross-coupled NOR network
        n1 = pydig_obj.combinational(
            maxOutSize=1,
            plot=False,
            blockID=f"N1 SR {SRLatch.__counter}",
            func=lambda x: SRLatch.__nor((x >> 1) & 1, x & 1),
            delay=0.1,
        )
        n2 = pydig_obj.combinational(
            maxOutSize=1,
            plot=False,
            blockID=f"N2 SR {SRLatch.__counter}",
            func=lambda x: SRLatch.__nor((x >> 1) & 1, x & 1),
            delay=0.1,
        )

        # SR encoding: bit0 = R, bit1 = S
        SR.output(0, 1) > n1.input()
        n2.output() > n1.input()

        n1.output() > n2.input()
        SR.output(1, 2) > n2.input()

        # Outputs
        n1.output() > o.input()
        n2.output() > self.__o_not.input()

    @staticmethod
    def __nor(a, b):
        """
        @param a : input signal
        """
        return (~(a | b)) & 0b1

    def getQNot(self):
        """
        @return Combinational : the ~Q output block
        """
        return self.__o_not


class DLatch(Comb):
    """
    Level-sensitive D latch built from the SR latch.
    """
    __counter = 0

    def __init__(self, pydig_obj: pd, clk: Clock, D: HOC, plot: bool = True):
        """
        @param pydig_obj : pydig object
        @param clk : the clock signal (Clock)
        @param D : the data signal (HasOutputConnections)
        @param plot : whether to plot this latch or not
        """
        checkType([(pydig_obj, pd), (clk, Clock), (D, HOC), (plot, bool)])

        DLatch.__counter += 1

        super().__init__(
            func=lambda x: x,
            env=pydig_obj.getEnv(),
            blockID=f"Q: D Latch {DLatch.__counter}",
            maxOutSize=1,
            delay=0,
            plot=plot,
        )
        o = pydig_obj.combinationalFromObject(self)
        self.__o_not = pydig_obj.combinational(
            maxOutSize=1,
            plot=False,
            blockID=f"~Q: D Latch {DLatch.__counter}",
            func=lambda x: x,
            delay=0,
        )

        D_not = pydig_obj.combinational(
            maxOutSize=1,
            plot=False,
            blockID=f"D Not D {DLatch.__counter}",
            func=lambda x: DLatch.__not(x),
            delay=0,
        )

        # R and S are ANDs of clk and D / ~D
        R = pydig_obj.combinational(
            maxOutSize=1,
            plot=False,
            blockID=f"R D {DLatch.__counter}",
            func=lambda x: (x >> 1) & (x & 1),
            delay=0,
        )
        S = pydig_obj.combinational(
            maxOutSize=1,
            plot=False,
            blockID=f"S D {DLatch.__counter}",
            func=lambda x: (x >> 1) & (x & 1),
            delay=0,
        )

        SR = pydig_obj.combinational(
            maxOutSize=1,
            plot=False,
            blockID=f"SR D {DLatch.__counter}",
            func=lambda x: x,
            delay=0,
        )

        self.__clk = clk

        # Wiring:
        D.output() > D_not.input()

        clk.output() > R.input()
        D_not.output() > R.input()

        clk.output() > S.input()
        D.output() > S.input()

        R.output() > SR.input()
        S.output() > SR.input()

        latch = SRLatch(pydig_obj, SR, plot=False)
        latch.output() > o.input()
        latch.getQNot().output() > self.__o_not.input()

    def getQNot(self):
        """
        @return Combinational : the ~Q output block
        """
        return self.__o_not

    @staticmethod
    def __not(x):
        """
        @param x : the input signal
        """
        return (~x) & 0b1

    def getScopeDump(self):
        """
        @return : combined scope dump of clock + Q
        """
        dic = self.__clk.getScopeDump()
        dic.update(self._scopeDump.getValues())
        return dic


# ---------- Integration PWM test ----------

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
    idx = header.index("PWM Output")

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

    PWM_Path = "Tests\\PWM.csv"
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


# ---------- Timing integration tests: SR latch & D latch ----------

def integration_timing_test_SRLatch_WithoutCSV():
    """
    Timing / functional test for SRLatch.

    We drive the SR inputs over time:
        t=0.0: S=0, R=0 (hold, initial)
        t=1.0: S=1, R=0 (set  -> Q=1, ~Q=0)
        t=2.5: S=0, R=0 (hold -> Q stays 1)
        t=4.0: S=0, R=1 (reset -> Q=0, ~Q=1)
        t=5.5: S=0, R=0 (hold -> Q stays 0)

    We check:
      - Q and ~Q are always complementary
      - Q sees both 0 and 1 during the run (set and reset observed)
    """
    print("Running integration_timing_test_1 (SRLatch)...")

    sim = pd("SRLatch_test")

    # SR encoded as 2 bits: bit0=R, bit1=S
    sr_pattern = [
        (0.0, 0b00),  # hold
        (1.0, 0b10),  # S=1,R=0 -> set
        (2.5, 0b00),  # hold
        (4.0, 0b01),  # S=0,R=1 -> reset
        (5.5, 0b00),  # hold
    ]

    sr_in = Input(
        inputList=sr_pattern,
        env=sim.getEnv(),
        plot=False,
        blockID="SR_input",
    )
    # manually register this Input with the pydig instance
    sim._pydig__components.append(sr_in)

    latch = SRLatch(sim, sr_in, plot=False)

    sim.run(until=8.0)

    q_series = get_series(latch, "Q: SR Latch")
    qn_series = get_series(latch.getQNot(), "~Q: SR Latch")

    if not q_series or not qn_series:
        print("FAIL: No scope data for SRLatch outputs.")
        return

    q_vals = [v for (_, v) in q_series]
    qn_vals = [v for (_, v) in qn_series]

    n = min(len(q_vals), len(qn_vals))
    comp_ok = all((q_vals[i] ^ qn_vals[i]) == 1 for i in range(n))

    if not comp_ok:
        print("FAIL: Q and ~Q are not complements at all times.")
        print("Q:", q_vals)
        print("~Q:", qn_vals)
        return

    if not (0 in q_vals and 1 in q_vals):
        print("FAIL: SRLatch Q never toggled between 0 and 1.")
        print("Q values:", q_vals)
        return

    print("PASS: integration_timing_test_1 (SRLatch functional & timing OK)")


def integration_timing_test_DLatch_WithoutCSV():
    """
    Timing / functional test for DLatch.

    Clock: timePeriod=4, onTime=2, initialValue=0
        -> low [0,2), high [2,4), low [4,6), high [6,8), ...

    D input:
        t=0.0: D=0
        t=1.0: D=1   (while clk low)  -> Q should still be 0 just before t=2
        t=3.0: D=0   (while clk high) -> Q should follow to 0 during same high
        t=5.0: D=1   (while clk low)  -> Q should stay 0 until next high (t>=6)

    We sample Q at:
        1.5  (clk low, after D=1)     -> Q == 0 (hold)
        2.5  (clk high, D=1)          -> Q == 1 (transparent)
        3.5  (clk high, D=0)          -> Q == 0 (transparent)
        5.5  (clk low, D=1)           -> Q == 0 (hold)
        6.5  (clk high, D=1)          -> Q == 1 (transparent again)
    """
    print("Running integration_timing_test_2 (DLatch)...")

    sim = pd("DLatch_test")

    clk = sim.clock(
        plot=False,
        blockID="clk_D",
        timePeriod=4,
        onTime=2,
        initialValue=0,
    )

    d_pattern = [
        (0.0, 0),
        (1.0, 1),  # toggle while clock low
        (3.0, 0),  # toggle while clock high
        (5.0, 1),  # toggle while clock low again
    ]
    D = Input(
        inputList=d_pattern,
        env=sim.getEnv(),
        plot=False,
        blockID="D_input",
    )
    sim._pydig__components.append(D)

    latch = DLatch(sim, clk, D, plot=False)

    sim.run(until=8.0)

    clk_series = get_series(clk, "Clock")
    d_series = get_series(D, "Input to")
    q_series = get_series(latch, "Q: D Latch")

    if not (clk_series and d_series and q_series):
        print("FAIL: Missing scope data for DLatch test.")
        return

    # helper lambda to assert equality
    def assert_eq(label, actual, expected):
        if actual != expected:
            print(f"FAIL: {label}: expected {expected}, got {actual}")
            raise AssertionError

    # Sample points
    q_1_5 = value_at(q_series, 1.5)   # clk low, D has become 1
    q_2_5 = value_at(q_series, 2.5)   # clk high, D=1
    d_2_5 = value_at(d_series, 2.5)

    q_3_5 = value_at(q_series, 3.5)   # clk high, D switched to 0 at t=3
    d_3_5 = value_at(d_series, 3.5)

    q_5_5 = value_at(q_series, 5.5)   # clk low, D=1
    d_5_5 = value_at(d_series, 5.5)

    q_6_5 = value_at(q_series, 6.5)   # clk high again, D=1
    d_6_5 = value_at(d_series, 6.5)

    if None in (q_1_5, q_2_5, q_3_5, q_5_5, q_6_5, d_2_5, d_3_5, d_5_5, d_6_5):
        print("FAIL: Some sampled values are None; timing resolution issue.")
        return

    # 1) While clock low, changes in D should not propagate immediately
    assert_eq("Q at t=1.5 (hold)", q_1_5, 0)

    # 2) While clock high, Q should follow D
    assert_eq("Q at t=2.5 (transparent, D)", q_2_5, d_2_5)
    assert_eq("Q at t=3.5 (transparent, D)", q_3_5, d_3_5)

    # 3) While clock low, D changes but Q holds
    assert_eq("Q vs D at t=5.5 (hold)", q_5_5, 0)
    assert_eq("D at t=5.5", d_5_5, 1)

    # 4) On next high phase, Q should catch up to D
    assert_eq("Q at t=6.5 (transparent after hold)", q_6_5, d_6_5)

    print("PASS: integration_timing_test_2 (DLatch level-sensitive behavior OK)")


if __name__ == "__main__":
    integration_testing_pwm()
    print("\n" + "=" * 60 + "\n")
    integration_testing_pwm_malformed()
    print("\n" + "=" * 60 + "\n")
    integration_timing_test_SRLatch_WithoutCSV()
    print("\n" + "=" * 60 + "\n")
    integration_timing_test_DLatch_WithoutCSV()


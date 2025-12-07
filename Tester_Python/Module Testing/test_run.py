"""
Tester for the pydig.run() method.
It verifies correct simulation execution, exception handling, 
and behavior across various circuit configurations.
"""

import sys
import os

# Add parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from pydig import pydig
import csv

def read_csv_values(path):
    vals = []
    with open(path, "r") as f:
        for row in csv.reader(f):
            if row and row[0].strip().lstrip("-").isdigit():
                vals.append(int(row[0]))
    return vals


def tester(sim, until, expected_exception=None):
    """
    sim : pydig instance
    until : time duration to run simulation
    expected_exception : if provided, test expects the run() to raise that exception
                         (e.g., SystemExit from printErrorAndExit)
    """
    try:
        sim.run(until=until)
        if expected_exception:
            print("FAIL: Expected exception", expected_exception.__name__)
        else:
            print("PASS: run() executed successfully.")
    except BaseException as e:
        # We use BaseException so we also catch SystemExit from sys.exit(1).
        if expected_exception and isinstance(e, expected_exception):
            print("PASS: Caught expected exception:", type(e).__name__, "-", e)
        elif expected_exception:
            print(
                "FAIL: Wrong exception type. Expected",
                expected_exception.__name__,
                "but got",
                type(e).__name__,
                ":",
                e,
            )
            raise
        else:
            print("FAIL: Unexpected exception during run():", type(e).__name__, "-", e)
            raise


def test_run_basic():
    sim = pydig("run_basic")

    src = sim.source("Tests/run_input1.csv", blockID="src1")
    out = sim.output(plot=False, blockID="out1")

    src.output() > out.input()

    tester(sim, until=20)


def test_run_with_dump():
    sim = pydig("run_dump")

    src = sim.source("Tests/run_input2.csv", blockID="src2")
    out = sim.output(plot=False, blockID="out2")

    src.output() > out.input()

    sim.generateCSV()

    tester(sim, until=20)


def test_run_unconnected_error():
    """
    Output is created but never connected to any input → pydig.run()
    should call printErrorAndExit -> sys.exit(1) -> SystemExit.
    """
    sim = pydig("run_unconnected")

    src = sim.source("Tests/run_input3.csv", blockID="src3")
    out = sim.output(plot=False, blockID="out3")

    # src.output() is never connected to out.input() -> out.isConnected() is False
    # pydig.run() should detect this and call printErrorAndExit.
    tester(sim, until=15, expected_exception=SystemExit)


def test_run_invalid_until():
    """
    Passing a non-int 'until' should hit checkType in pydig.run()
    -> printErrorAndExit -> sys.exit(1) -> SystemExit.
    """
    sim = pydig("run_invalid_until")

    src = sim.source("Tests/run_input4.csv", blockID="src4")
    out = sim.output(plot=False, blockID="out4")

    src.output() > out.input()

    tester(sim, until="abc", expected_exception=SystemExit)


def test_run_full_pipeline():
    sim = pydig("run_full")

    src = sim.source("Tests/run_input5.csv", blockID="src5")

    comb = sim.combinational(
        maxOutSize=1,
        blockID="comb5",
        func=lambda x: (x + 1) & 1,
    )

    out = sim.output(plot=False, blockID="out5")

    src.output() > comb.input()
    comb.output() > out.input()

    tester(sim, until=30)


if __name__ == "__main__":
    test_run_basic()
    test_run_with_dump()
    test_run_unconnected_error()
    test_run_invalid_until()
    test_run_full_pipeline()

"""
Tester for the pydig.run() method.
It verifies correct simulation execution, exception handling, 
and behavior across various circuit configurations.
"""

from pydig import pydig
import csv



def read_csv_values(path):
    vals = []
    with open(path, "r") as f:
        for row in csv.reader(f):
            if row and row[0].strip().isdigit():
                vals.append(int(row[0]))
    return vals




def tester(sim, until, expected_exception=None):
    """
    sim : pydig instance
    until : time duration to run simulation
    expected_exception : if provided, test expects the run() to raise that exception
    """

    try:
        sim.run(until=until)
        if expected_exception:
            print("FAIL: Expected exception", expected_exception)
        else:
            print("PASS: run() executed successfully.")
    except Exception as e:
        if expected_exception and isinstance(e, expected_exception):
            print("PASS: Caught expected exception:", e)
        elif expected_exception:
            print("FAIL: Wrong exception type. Expected", expected_exception, "but got", type(e).__name__, ":", e)
            raise
        else:
            print("FAIL: Unexpected exception during run():", e)
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
    sim = pydig("run_unconnected")

    src = sim.source("Tests/run_input3.csv", blockID="src3")
    out = sim.output(plot=False, blockID="out3")


    tester(sim, until=15, expected_exception=Exception)



def test_run_invalid_until():
    sim = pydig("run_invalid_until")

    src = sim.source("Tests/run_input4.csv", blockID="src4")
    out = sim.output(plot=False, blockID="out4")

    src.output() > out.input()

    tester(sim, until="abc", expected_exception=Exception)


def test_run_full_pipeline():
    sim = pydig("run_full")

    src = sim.source("Tests/run_input5.csv", blockID="src5")

    comb = sim.combinational(
        maxOutSize=1,
        blockID="comb5",
        func=lambda x: (x + 1) & 1  
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

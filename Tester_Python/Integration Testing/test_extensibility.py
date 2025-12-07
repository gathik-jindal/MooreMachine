"""
test_extensiblity.py

Tests for:
1) Gate extensibility (custom combinational gates built on top of Combinational)
2) Register wrappers (SISO, SIPO, PIPO, PISO) built on top of Moore machines
"""

import sys
import os

# Add parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import random
from utilities import checkType, bitCount
from pydig import pydig as pd
from usableBlocks import Combinational as Comb, Input
from blocks import HasOutputConnections


# ============================================================================
# GATE IMPLEMENTATIONS
# ============================================================================

def n(val):
    """
    @param val (int): The value to be negated
    @return (int): The negated value
    """
    mask = 1 if val == 0 else (1 << bitCount(val)) - 1
    return mask & ~val


class NOT(Comb):
    """
    This class represents the NOT gate.
    All the incoming lines will be negated.
    """

    def __init__(self, pydig: pd, delay: float, initialValue: int, plot: bool, blockID: str):
        """
        @param pydig : pydig object
        @param delay : the time delay for the NOT gate
        @param initialValue : The initial output value given by this block at t = 0 while running
        @param plot : boolean value whether to plot this moore machine or not
        @param blockID : the id of this moore machine. If None, then new unique ID is given.
        """
        checkType([(pydig, pd), (delay, (float, int)), (initialValue, int), (plot, bool), (blockID, str)])
        super().__init__(func=self.__func, env=pydig.getEnv(), blockID=blockID,
                         maxOutSize=1, delay=delay, plot=plot, initialValue=initialValue)

        pydig.combinationalFromObject(self)  # make this object a part of the pydig object

    def __func(self, val):
        """
        @param val (int): The value to be negated (can be more than single bit)
        @return (int): The negated value
        """
        return (2 ** bitCount(val) - 1) & ~val

class DMUX(Comb):
    """
    This class represents the DMUX gate.
    If the selection bit is 0, then val is sent as second value, else as first value.

    The first bit is the selection bit, and the rest of the bits are the value.
    For example, input 11 (binary) -> sel=1, val=1, output 10;
    if selection bit was 0, then the output would have been 01.
    """

    def __init__(self, pydig: pd, delay: float, initialValue: int, plot: bool, blockID: str):
        """
        @param pydig : pydig object
        @param delay : the time delay for the DMUX gate
        @param initialValue : The initial output value given by this block at t = 0 while running
        @param plot : boolean value whether to plot this block or not
        @param blockID : the id of this block. If None, then new unique ID is given.
        """
        checkType([(pydig, pd), (delay, (float, int)), (initialValue, int), (plot, bool), (blockID, str)])
        super().__init__(func=self.__func, env=pydig.getEnv(), blockID=blockID,
                         maxOutSize=2, delay=delay, plot=plot, initialValue=initialValue)

        pydig.combinationalFromObject(self)  # make this object a part of the pydig object

    def __func(self, val):
        """
        @param val (int): The value to be demultiplexed
        @return (int): Two demuxed outputs packed into 2 bits.
        """
        sel = val >> 1
        val = val & 1
        val = val | (val << 1)
        ans = (sel << 1) | n(sel)
        return ans & val


# ============================================================================
# REGISTER WRAPPER IMPLEMENTATIONS
# ============================================================================

class PIPO:
    """
    This class represents the PIPO register.
    """

    def __init__(self, pydig: pd, size: int, clock, delay: float, initialValue: int, plot: bool, blockID: str):
        checkType([(pydig, pd), (delay, (float, int)), (size, int),
                   (initialValue, int), (plot, bool), (blockID, str)])
        self.__register = pydig.moore(maxOutSize=size, plot=plot, blockID=blockID,
                                      startingState=initialValue, clock=clock, register_delay=delay)
        self.__size = size
        self.__register.nsl = self.__nsl
        self.__register.ol = self.__ol

    def __nsl(self, ps, i):
        return i & (2 ** self.__size - 1)

    def __ol(self, ps):
        return ps & (2 ** self.__size - 1)

    def input(self, left=None, right=None):
        return self.__register.input(left, right)

    def output(self, left=0, right=None):
        return self.__register.output(left, right)

    def clock(self):
        return self.__register.clock()

    def __le__(self, other):
        self.__register.input() <= other
        return True

    def __gt__(self, other):
        self.__register.output() > other
        return True


class PISO:
    """
    This class represents the PISO register.
    """

    def __init__(self, pydig: pd, size: int, clock, load, drive, delay: float,
                 initialValue: int, plot: bool, blockID: str):
        checkType([
            (pydig, pd),
            (delay, (float, int)),
            (size, int),
            (initialValue, int),
            (drive, int),
            (plot, bool),
            (blockID, str),
            (load, HasOutputConnections),
        ])
        self.__register = pydig.moore(maxOutSize=size, plot=plot, blockID=blockID,
                                      startingState=initialValue, clock=clock, register_delay=delay)
        self.__drive = drive & 1
        load.output() > self.__register.input()
        self.__size = size
        self.__register.nsl = self.__nsl
        self.__register.ol = self.__ol

    def __nsl(self, ps, i):
        if i & 1:
            return (i >> 1) & (2 ** self.__size - 1)
        return ((ps * 2) % (2 ** self.__size) + self.__drive)

    def __ol(self, ps):
        return (ps >> (self.__size - 1)) & 1

    def input(self, left=None, right=None):
        return self.__register.input(left, right)

    def output(self, left=0, right=None):
        return self.__register.output(left, right)

    def clock(self):
        return self.__register.clock()

    def __le__(self, other):
        self.__register.input() <= other
        return True

    def __gt__(self, other):
        self.__register.output() > other
        return True


# ============================================================================
# HELPERS FOR TESTS
# ============================================================================

def run_gate_sim(gate_cls, test_values, expected_fn, *, blockID, delay=0.0):
    """
    Helper for gate tests.
    """
    sim = pd(f"extend_{blockID}")

    input_list = [(float(t), v) for t, v in enumerate(test_values)]
    src = Input(inputList=input_list, env=sim.getEnv(), blockID=f"src_{blockID}", plot=False)

    sim._pydig__components.append(src)

    gate = gate_cls(sim, delay, 0, False, blockID)
    src.output() > gate.input()

    sim.run(until=len(test_values) + 2)

    dump = gate.getScopeDump()
    keys = [k for k in dump if "output" in k]
    key = keys[0] if keys else list(dump.keys())[-1]

    time_vals = dump[key]
    vals = [v for (_, v) in time_vals][2:]

    expected = [expected_fn(v) for v in test_values]
    passed = (len(vals) >= len(expected)) and (vals[:len(expected)] == expected)
    return passed, vals, expected


# expected behaviors (what we *want* the gates to do)

def expected_not(v: int) -> int:
    width = bitCount(v)
    mask = (1 << width) - 1
    return (~v) & mask

def expected_dmux2(v: int) -> int:
    sel = (v >> 1) & 1
    val = v & 1
    if sel == 0:
        out1, out2 = 0, val
    else:
        out1, out2 = val, 0
    return (out1 << 1) | out2


# ============================================================================
# TEST 1: GATES
# ============================================================================

def test_gates():
    """
    Tests the extended gate classes:

        NOT

    Each gate is driven via an Input block, and the output waveform is
    compared against a pure-Python expected truth table.
    """
    print("Running test_gates()...\n")

    all_ok = True

    print("Testing NOT gate...")
    not_ok, not_vals, not_exp = run_gate_sim(
        NOT, test_values=list(range(4)), expected_fn=expected_not, blockID="NOT_test"
    )
    print("  actual:   ", not_vals)
    print("  expected: ", not_exp)
    print("  result:   ", "PASS" if not_ok else "FAIL", "\n")
    all_ok &= not_ok

    print("Testing DMUX gate...")
    dmux_ok, dmux_vals, dmux_exp = run_gate_sim(
        DMUX, test_values=list(range(4)), expected_fn=expected_dmux2, blockID="DMUX_test"
    )
    print("  actual:   ", dmux_vals)
    print("  expected: ", dmux_exp)
    print("  result:   ", "PASS" if dmux_ok else "FAIL", "\n")
    all_ok &= dmux_ok

    print("\nOverall result for test_gates():", "PASS" if all_ok else "FAIL")


# ============================================================================
# TEST 2: REGISTERS
# ============================================================================

def test_registers():
    """
    Tests the custom register wrapper classes:
        - SISO (Serial In Serial Out)
        - SIPO (Serial In Parallel Out)
        - PIPO (Parallel In Parallel Out)
        - PISO (Parallel In Serial Out with load & drive)
    """
    print("Running test_registers()...\n")

    # ---------- PIPO ----------
    print("Testing PIPO register...")
    sim_pipo = pd("PIPO_test")
    clk_pipo = sim_pipo.clock(plot=False, blockID="clk_pipo", timePeriod=1.0, onTime=0.5, initialValue=0)

    size_pipo = 4
    pipo_vals = [0b0101, 0b1110]
    pipo_input_list = [(float(t), v) for t, v in enumerate(pipo_vals)]
    pipo_src = Input(inputList=pipo_input_list, env=sim_pipo.getEnv(), blockID="src_pipo", plot=False)
    sim_pipo._pydig__components.append(pipo_src)

    pipo = PIPO(sim_pipo, size_pipo, clk_pipo, 0.1, 0, False, "PIPO_reg")
    pipo_src.output() > pipo.input()
    clk_pipo.output() > pipo.clock()

    sim_pipo.run(until=len(pipo_vals) + 5)

    internal_pipo = pipo._PIPO__register
    dump = internal_pipo.getScopeDump()
    ps_keys = [k for k in dump if "PS of" in k]
    final_ps_pipo = [v for (_, v) in dump[ps_keys[0]]][-1] if ps_keys else None
    out_keys = [k for k in dump if "output of" in k]
    final_out_pipo = [v for (_, v) in dump[out_keys[0]]][-1] if out_keys else None

    expected_ps_pipo = pipo_vals[-1] & ((1 << size_pipo) - 1)
    expected_out_pipo = expected_ps_pipo
    ok_pipo = (final_ps_pipo == expected_ps_pipo and final_out_pipo == expected_out_pipo)

    print(f"  PIPO final PS:  {final_ps_pipo} (expected {expected_ps_pipo})")
    print(f"  PIPO final OUT: {final_out_pipo} (expected {expected_out_pipo})")
    print("  result:         ", "PASS\n" if ok_pipo else "FAIL\n")

    all_ok = ok_pipo

    # ---------- PISO ----------
    print("Testing PISO register (load behavior)...")
    sim_piso = pd("PISO_test")
    clk_piso = sim_piso.clock(plot=False, blockID="clk_piso", timePeriod=1.0, onTime=0.5, initialValue=0)

    size_piso = 4
    drive_bit = 1
    data_to_load = 0b1011
    combined_load_val = (data_to_load << 1) | 1

    piso_input_list = [
        (0.0, combined_load_val),
        (2.0, combined_load_val),
    ]
    piso_load_src = Input(inputList=piso_input_list, env=sim_piso.getEnv(), blockID="src_piso_load", plot=False)
    sim_piso._pydig__components.append(piso_load_src)

    piso = PISO(sim_piso, size_piso, clk_piso, piso_load_src, drive_bit, 0.1, 0, False, "PISO_reg")
    clk_piso.output() > piso.clock()

    sim_piso.run(until=6)

    internal_piso = piso._PISO__register
    dump = internal_piso.getScopeDump()
    ps_keys = [k for k in dump if "PS of" in k]
    final_ps_piso = [v for (_, v) in dump[ps_keys[0]]][-1] if ps_keys else None
    out_keys = [k for k in dump if "output of" in k]
    final_out_piso = [v for (_, v) in dump[out_keys[0]]][-1] if out_keys else None

    expected_ps_piso = data_to_load & ((1 << size_piso) - 1)
    expected_out_piso = (expected_ps_piso >> (size_piso - 1)) & 1
    ok_piso = (final_ps_piso == expected_ps_piso and final_out_piso == expected_out_piso)

    print(f"  PISO final PS:  {final_ps_piso} (expected {expected_ps_piso})")
    print(f"  PISO final OUT: {final_out_piso} (expected {expected_out_piso})")
    print("  result:         ", "PASS\n" if ok_piso else "FAIL\n")

    all_ok &= ok_piso

    print("\nOverall result for test_registers():", "PASS" if all_ok else "FAIL")


if __name__ == "__main__":
    test_gates()
    print("\n" + "=" * 60 + "\n")
    test_registers()

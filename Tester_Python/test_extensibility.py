"""
test_extensiblity.py

Tests for:
1) Gate extensibility (custom combinational gates built on top of Combinational)
2) Register wrappers (SISO, SIPO, PIPO, PISO) built on top of Moore machines
"""

import os
import sys
import random

# directory reach (same pattern as your reference files)
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

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


class AND(Comb):
    """
    This class represents the AND gate.
    Half the incoming lines will be ANDed with the other half.

    Lets say the incoming bits are: 10101100
    Then the first 4 bits will be ANDed with the last 4 bits, in this order: 1010 & 1100
    """

    def __init__(self, pydig: pd, delay: float, initialValue: int, plot: bool, blockID: str):
        """
        @param pydig : pydig object
        @param delay : the time delay for the and gate
        @param initialValue : The initial output value given by this block at t = 0 while running
        @param plot : boolean value whether to plot this block or not
        @param blockID : the id of this block. If None, then new unique ID is given.
        """
        checkType([(pydig, pd), (delay, (float, int)), (initialValue, int), (plot, bool), (blockID, str)])
        super().__init__(func=self.__func, env=pydig.getEnv(), blockID=blockID,
                         maxOutSize=1, delay=delay, plot=plot, initialValue=initialValue)

        pydig.combinationalFromObject(self)  # make this object a part of the pydig object

    def __func(self, val):
        """
        @param val (int): The value that's going to be used to AND
        @return (int): The result of the AND operation
        """
        ans = 1
        while val:
            ans = ans & (val % 2)
            val = val >> 1
        return ans


class OR(Comb):
    """
    This class represents the OR gate.
    Half the incoming lines will be ORed with the other half.

    Lets say the incoming bits are: 10101100
    Then the first 4 bits will be ORed with the last 4 bits, in this order: 1010 & 1100
    """

    def __init__(self, pydig: pd, delay: float, initialValue: int, plot: bool, blockID: str):
        """
        @param pydig : pydig object
        @param delay : the time delay for the OR gate
        @param initialValue : The initial output value given by this block at t = 0 while running
        @param plot : boolean value whether to plot this block or not
        @param blockID : the id of this block. If None, then new unique ID is given.
        """
        checkType([(pydig, pd), (delay, (float, int)), (initialValue, int), (plot, bool), (blockID, str)])
        super().__init__(func=self.__func, env=pydig.getEnv(), blockID=blockID,
                         maxOutSize=1, delay=delay, plot=plot, initialValue=initialValue)

        pydig.combinationalFromObject(self)  # make this object a part of the pydig object

    def __func(self, val):
        """
        @param val (int): The value to be ORed
        @return (int): The result of the OR operation
        """
        ans = 1
        while val:
            ans = ans | (val % 2)
            val = val >> 1
        return ans


class XOR(Comb):
    """
    This class represents the XOR gate.
    Half the incoming lines will be XORed with the other half.

    Lets say the incoming bits are: 10101100
    Then the first 4 bits will be XORed with the last 4 bits, in this order: 1010 & 1100
    """

    def __init__(self, pydig: pd, delay: float, initialValue: int, plot: bool, blockID: str):
        """
        @param pydig : pydig object
        @param delay : the time delay for the XOR gate
        @param initialValue : The initial output value given by this block at t = 0 while running
        @param plot : boolean value whether to plot this block or not
        @param blockID : the id of this block. If None, then new unique ID is given.
        """
        checkType([(pydig, pd), (delay, (float, int)), (initialValue, int), (plot, bool), (blockID, str)])
        super().__init__(func=self.__func, env=pydig.getEnv(), blockID=blockID,
                         maxOutSize=1, delay=delay, plot=plot, initialValue=initialValue)

        pydig.combinationalFromObject(self)  # make this object a part of the pydig object

    def __func(self, val):
        """
        @param val (int): The value to be XORed
        @return (int): The result of the XOR operation
        """
        ans = 1
        while val:
            ans = ans ^ (val % 2)
            val = val >> 1
        return ans


class NAND(Comb):
    """
    This class represents the NAND gate.
    """

    def __init__(self, pydig: pd, delay: float, initialValue: int, plot: bool, blockID: str):
        """
        @param pydig : pydig object
        @param delay : the time delay for the NAND gate
        @param initialValue : The initial output value given by this block at t = 0 while running
        @param plot : boolean value whether to plot this block or not
        @param blockID : the id of this block. If None, then new unique ID is given.
        """
        self.__andGate = AND(pydig, delay, initialValue, False, blockID + str(random.randint(10, 10000)))
        self.__notGate = NOT(pydig, 0, initialValue, plot, blockID)

        self.__andGate.output() > self.__notGate.input()

    def input(self, left=None, right=None):
        """
        @return obj : instance of the andGate object
        """
        return self.__andGate.input(left, right)

    def output(self, left=0, right=None):
        """
        @return obj : instance of the notGate object
        """
        return self.__notGate.output(left, right)

    def getScopeDump(self):
        """
        @return dict : the scope dump values for this block.
        """
        return self.__notGate.getScopeDump()


class NOR(Comb):
    """
    This class represents the NOR gate.
    """

    def __init__(self, pydig: pd, delay: float, initialValue: int, plot: bool, blockID: str):
        """
        @param pydig : pydig object
        @param delay : the time delay for the NOR gate
        @param initialValue : The initial output value given by this block at t = 0 while running
        @param plot : boolean value whether to plot this block or not
        @param blockID : the id of this block. If None, then new unique ID is given.
        """
        self.__orGate = OR(pydig, delay, initialValue, False, blockID + str(random.randint(10, 10000)))
        self.__notGate = NOT(pydig, 0, initialValue, plot, blockID)

        self.__orGate.output() > self.__notGate.input()

    def input(self, left=None, right=None):
        """
        @return obj : instance of the orGate object
        """
        return self.__orGate.input(left, right)

    def output(self, left=0, right=None):
        """
        @return obj : instance of the notGate object
        """
        return self.__notGate.output(left, right)

    def getScopeDump(self):
        """
        @return dict : the scope dump values for this block.
        """
        return self.__notGate.getScopeDump()


class XNOR(Comb):
    """
    This class represents the XNOR gate.
    """

    def __init__(self, pydig: pd, delay: float, initialValue: int, plot: bool, blockID: str):
        """
        @param pydig : pydig object
        @param delay : the time delay for the XNOR gate
        @param initialValue : The initial output value given by this block at t = 0 while running
        @param plot : boolean value whether to plot this block or not
        @param blockID : the id of this block. If None, then new unique ID is given.
        """
        self.__xorGate = XOR(pydig, delay, initialValue, False, blockID + str(random.randint(10, 10000)))
        self.__notGate = NOT(pydig, 0, initialValue, plot, blockID)

        self.__xorGate.output() > self.__notGate.input()

    def input(self, left=None, right=None):
        """
        @return obj : instance of the xorGate object
        """
        return self.__xorGate.input(left, right)

    def output(self, left=0, right=None):
        """
        @return obj : instance of the notGate object
        """
        return self.__notGate.output(left, right)

    def getScopeDump(self):
        """
        @return dict : the scope dump values for this block.
        """
        return self.__notGate.getScopeDump()


class MUX(Comb):
    """
    This class represents the MUX gate.
    If the selection bit is 0, then the first value is selected, else the second value is selected.

    The first bit is the selection bit, and the second and third bits are values (from left to right).
    """

    def __init__(self, pydig: pd, delay: float, initialValue: int, plot: bool, blockID: str):
        """
        @param pydig : pydig object
        @param delay : the time delay for the MUX gate
        @param initialValue : The initial output value given by this block at t = 0 while running
        @param plot : boolean value whether to plot this block or not
        @param blockID : the id of this block. If None, then new unique ID is given.
        """
        checkType([(pydig, pd), (delay, (float, int)), (initialValue, int), (plot, bool), (blockID, str)])
        super().__init__(func=self.__func, env=pydig.getEnv(), blockID=blockID,
                         maxOutSize=1, delay=delay, plot=plot, initialValue=initialValue)

        pydig.combinationalFromObject(self)  # make this object a part of the pydig object

    def __func(self, val):
        """
        @param val (int): The value to be MUXed
        @return (int): The result of the MUX operation
        """
        sel = val >> 2
        val = val & 3
        val1 = val >> 1
        val2 = val & 1
        mask = n(sel)

        return (val1 & n(mask)) | (val2 & mask)


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
# REGISTER WRAPPER IMPLEMENTATIONS (from your reference code)
# ============================================================================

class SISO:
    """
    This class represents the SISO register.
    """

    def __init__(self, pydig: pd, size: int, clock, delay: float, initialValue: int, plot: bool, blockID: str):
        """
        @param pydig : pydig object
        @param delay : the time delay for each register in the SISO block.
        @param size : the number of registers in the SISO block
        @param initialValue : The initial output value given by each register
        @param plot : boolean value whether to plot this block or not
        @param blockID : id of this block.
        """
        checkType([(pydig, pd), (delay, (float, int)), (size, int),
                   (initialValue, int), (plot, bool), (blockID, str)])
        self.__register = pydig.moore(maxOutSize=1, plot=plot, blockID=blockID,
                                      startingState=initialValue, clock=clock, register_delay=delay)
        self.__size = size
        self.__register.nsl = self.__nsl
        self.__register.ol = self.__ol

    def __nsl(self, ps, i):
        return ((ps * 2) % (2 ** self.__size) + (i & 1))

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


class SIPO:
    """
    This class represents the SIPO register.
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
        return ((ps * 2) % (2 ** self.__size) + (i & 1))

    def __ol(self, ps):
        k = self.__size
        ans = 0
        while k:
            k -= 1
            ans = ans << 1
            ans += ps & 1
            ps = ps >> 1
        return ans

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
    vals = [v for (_, v) in time_vals][1:]

    expected = [expected_fn(v) for v in test_values]
    passed = (len(vals) >= len(expected)) and (vals[:len(expected)] == expected)
    return passed, vals, expected


# expected behaviors (what we *want* the gates to do)

def expected_not(v: int) -> int:
    width = bitCount(v)
    mask = (1 << width) - 1
    return (~v) & mask


def expected_and2(v: int) -> int:
    b = v & 1
    a = (v >> 1) & 1
    return a & b


def expected_or2(v: int) -> int:
    b = v & 1
    a = (v >> 1) & 1
    return a | b


def expected_xor2(v: int) -> int:
    b = v & 1
    a = (v >> 1) & 1
    return a ^ b


def expected_nand2(v: int) -> int:
    return 1 - expected_and2(v)


def expected_nor2(v: int) -> int:
    return 1 - expected_or2(v)


def expected_xnor2(v: int) -> int:
    return 1 - expected_xor2(v)


def expected_mux3(v: int) -> int:
    sel = (v >> 2) & 1
    val1 = (v >> 1) & 1
    val2 = v & 1
    return val1 if sel == 0 else val2


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

        NOT, AND, OR, XOR, NAND, NOR, XNOR, MUX, DMUX

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

    print("Testing AND gate...")
    and_ok, and_vals, and_exp = run_gate_sim(
        AND, test_values=list(range(4)), expected_fn=expected_and2, blockID="AND_test"
    )
    print("  actual:   ", and_vals)
    print("  expected: ", and_exp)
    print("  result:   ", "PASS" if and_ok else "FAIL", "\n")
    all_ok &= and_ok

    print("Testing OR gate...")
    or_ok, or_vals, or_exp = run_gate_sim(
        OR, test_values=list(range(4)), expected_fn=expected_or2, blockID="OR_test"
    )
    print("  actual:   ", or_vals)
    print("  expected: ", or_exp)
    print("  result:   ", "PASS" if or_ok else "FAIL", "\n")
    all_ok &= or_ok

    print("Testing XOR gate...")
    xor_ok, xor_vals, xor_exp = run_gate_sim(
        XOR, test_values=list(range(4)), expected_fn=expected_xor2, blockID="XOR_test"
    )
    print("  actual:   ", xor_vals)
    print("  expected: ", xor_exp)
    print("  result:   ", "PASS" if xor_ok else "FAIL", "\n")
    all_ok &= xor_ok

    print("Testing NAND gate...")
    nand_ok, nand_vals, nand_exp = run_gate_sim(
        NAND, test_values=list(range(4)), expected_fn=expected_nand2, blockID="NAND_test"
    )
    print("  actual:   ", nand_vals)
    print("  expected: ", nand_exp)
    print("  result:   ", "PASS" if nand_ok else "FAIL", "\n")
    all_ok &= nand_ok

    print("Testing NOR gate...")
    nor_ok, nor_vals, nor_exp = run_gate_sim(
        NOR, test_values=list(range(4)), expected_fn=expected_nor2, blockID="NOR_test"
    )
    print("  actual:   ", nor_vals)
    print("  expected: ", nor_exp)
    print("  result:   ", "PASS" if nor_ok else "FAIL", "\n")
    all_ok &= nor_ok

    print("Testing XNOR gate...")
    xnor_ok, xnor_vals, xnor_exp = run_gate_sim(
        XNOR, test_values=list(range(4)), expected_fn=expected_xnor2, blockID="XNOR_test"
    )
    print("  actual:   ", xnor_vals)
    print("  expected: ", xnor_exp)
    print("  result:   ", "PASS" if xnor_ok else "FAIL", "\n")
    all_ok &= xnor_ok

    print("Testing MUX gate...")
    mux_ok, mux_vals, mux_exp = run_gate_sim(
        MUX, test_values=list(range(8)), expected_fn=expected_mux3, blockID="MUX_test"
    )
    print("  actual:   ", mux_vals)
    print("  expected: ", mux_exp)
    print("  result:   ", "PASS" if mux_ok else "FAIL", "\n")
    all_ok &= mux_ok

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

    # ---------- SISO ----------
    print("Testing SISO register...")
    sim_siso = pd("SISO_test")
    clk_siso = sim_siso.clock(plot=False, blockID="clk_siso", timePeriod=1.0, onTime=0.5, initialValue=0)

    siso_bits = [1, 0, 1, 1]
    siso_input_list = [(float(t), b) for t, b in enumerate(siso_bits)]
    siso_src = Input(inputList=siso_input_list, env=sim_siso.getEnv(), blockID="src_siso", plot=False)
    sim_siso._pydig__components.append(siso_src)

    size_siso = 4
    siso = SISO(sim_siso, size_siso, clk_siso, 0.1, 0, False, "SISO_reg")
    siso_src.output() > siso.input()
    clk_siso.output() > siso.clock()

    sim_siso.run(until=len(siso_bits) + 5)

    internal_siso = siso._SISO__register
    dump = internal_siso.getScopeDump()
    ps_keys = [k for k in dump if "PS of" in k]
    final_ps = [v for (_, v) in dump[ps_keys[0]]][-1] if ps_keys else None
    out_keys = [k for k in dump if "output of" in k]
    final_out = [v for (_, v) in dump[out_keys[0]]][-1] if out_keys else None

    expected_ps = 0b1011
    expected_out = 1
    ok_siso = (final_ps == expected_ps and final_out == expected_out)
    print(f"  SISO final PS:  {final_ps} (expected {expected_ps})")
    print(f"  SISO final OUT: {final_out} (expected {expected_out})")
    print("  result:         ", "PASS\n" if ok_siso else "FAIL\n")

    all_ok = ok_siso

    # ---------- SIPO ----------
    print("Testing SIPO register...")
    sim_sipo = pd("SIPO_test")
    clk_sipo = sim_sipo.clock(plot=False, blockID="clk_sipo", timePeriod=1.0, onTime=0.5, initialValue=0)

    sipo_bits = [1, 0, 1, 1]
    sipo_input_list = [(float(t), b) for t, b in enumerate(sipo_bits)]
    sipo_src = Input(inputList=sipo_input_list, env=sim_sipo.getEnv(), blockID="src_sipo", plot=False)
    sim_sipo._pydig__components.append(sipo_src)

    size_sipo = 4
    sipo = SIPO(sim_sipo, size_sipo, clk_sipo, 0.1, 0, False, "SIPO_reg")
    sipo_src.output() > sipo.input()
    clk_sipo.output() > sipo.clock()

    sim_sipo.run(until=len(sipo_bits) + 5)

    internal_sipo = sipo._SIPO__register
    dump = internal_sipo.getScopeDump()
    ps_keys = [k for k in dump if "PS of" in k]
    final_ps_sipo = [v for (_, v) in dump[ps_keys[0]]][-1] if ps_keys else None
    out_keys = [k for k in dump if "output of" in k]
    final_out_sipo = [v for (_, v) in dump[out_keys[0]]][-1] if out_keys else None

    expected_ps_sipo = 0b1011
    ok_sipo = (final_ps_sipo == expected_ps_sipo and final_out_sipo is not None and final_out_sipo != 0)
    print(f"  SIPO final PS:  {final_ps_sipo} (expected {expected_ps_sipo})")
    print(f"  SIPO final OUT: {final_out_sipo} (non-zero expected)")
    print("  result:         ", "PASS\n" if ok_sipo else "FAIL\n")

    all_ok &= ok_sipo

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

    all_ok &= ok_pipo

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

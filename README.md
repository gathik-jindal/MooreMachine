# Moore Machine Simulator

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Java 11+](https://img.shields.io/badge/java-11+-orange.svg)](https://www.oracle.com/java/)
[![Code style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](https://github.com/gathik-jindal/MooreMachine)

A comprehensive **Python** and **Java** implementation of Moore Machine finite state machine simulators with interactive graphical user interface, discrete event simulation, and comprehensive building block library.

[Features](#features) • [Installation](#installation) • [Quick Start](#quick-start) • [Documentation](#documentation) • [Contributing](#contributing) • [License](#license)

</div>

---

## Overview

A **Moore Machine** is a type of finite state machine (FSM) where outputs are determined solely by the current state, independent of inputs or transitions. This simulator provides a flexible framework for designing, simulating, and visualizing Moore Machine systems with professional-grade tools.

### Key Characteristics

- **States**: Finite set of discrete states the system can occupy
- **Inputs**: External signals that trigger state transitions
- **Outputs**: State-dependent outputs independent of input timing
- **Deterministic**: Output uniquely determined by current state

## Features

### 🐍 Python Simulation Engine

- ⚡ Discrete event simulation powered by [SimPy](https://simpy.readthedocs.io/)
- 📊 Support for diverse building blocks (counters, latches, gates)
- 📁 CSV/TXT/XLSX input file support
- 📈 Matplotlib-based data visualization
- 🔧 Extensible block architecture for custom components
- 🎯 Operator overloading for intuitive block connections

### 🎨 Interactive GUI (Java)

- 🖱️ Visual circuit design with drag-and-drop
- ⚙️ Real-time block parameter configuration
- 🔄 Auto-code generation from diagrams
- 💾 Drawing export and persistence
- 🎪 Zoom and pan for complex circuits

### 🏗️ Building Blocks Library

| Component                | Description                                  |
| ------------------------ | -------------------------------------------- |
| **Bit Counters**         | 1-4 bit enabled counters with terminal count |
| **Freeze Counter**       | Counter with dynamic freeze capability       |
| **Synchronous Counters** | Clock-driven modulo & period-based counters  |
| **Latches**              | SR and D latch implementations               |
| **Combinational Logic**  | Custom combinational blocks with delays      |
| **I/O Blocks**           | Input sources and output sinks               |

## Quick Start

### Prerequisites

- **Python 3.8** or higher
- **Java 11** or higher (for GUI)
- **pip** package manager

### Installation

```bash
# Clone the repository
git clone https://github.com/gathik-jindal/MooreMachine.git
cd MooreMachine

# Create and activate virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Dependencies

| Package    | Version | Purpose                          |
| ---------- | ------- | -------------------------------- |
| simpy      | ≥4.1.1  | Discrete event simulation engine |
| matplotlib | ≥3.8.2  | Data visualization               |
| pandas     | ≥2.2.2  | Data manipulation & CSV handling |
| openpyxl   | ≥3.1.2  | Excel file support               |

## Usage

### Python Simulation - Basic Example

```python
import pydig

# Create simulation environment
simulator = pydig.pydig(name="MySimulation")

# Define Moore Machine logic
def next_state_logic(current_state, input_value):
    return (current_state + input_value) & 0xFF

def output_logic(current_state):
    return current_state

# Create components
clock = simulator.clock(timePeriod=1.0, onTime=0.5, blockID="clk")
source = simulator.source(filePath="input.csv", blockID="source")
moore = simulator.moore(maxOutSize=8, blockID="FSM")
output = simulator.output(blockID="result")

# Configure Moore Machine
moore.nsl = next_state_logic
moore.ol = output_logic

# Connect components
clock.output() > moore.clock()
source.output() > moore.input()
moore.output() > output.input()

# Run simulation
simulator.generateCSV()
simulator.run(until=100)
```

### Using Building Blocks

```python
from BuildingBlocks.BitCounters import Enabled4BitCounterWithTC
from BuildingBlocks.Latches import DLatch

# 4-bit counter with terminal count output
counter = Enabled4BitCounterWithTC(
    pydig=simulator,
    enable=enable_signal,
    clock=clock,
    plot=True
)

# D-Latch for storage
latch = DLatch(
    pydig=simulator,
    D=data_input,
    clock=clock,
    plot=True
)
```

### Input File Format

The simulator supports **CSV**, **TXT**, and **XLSX** formats:

```csv
time,input1,input2,input3
---,3,3,3
0.1,1,2,0
1.1,2,4,5
2.1,3,5,2
3.1,4,5,0
4.1,5,0,0
```

**Format Rules:**

- Line 1: Header (ignored)
- Line 2: Bit widths for each field
- Lines 3+: Input data with timestamps

### GUI Usage

#### Launch the Graphical Interface

```bash
java -jar FiniteStateMachineSimulation.jar
```

#### Building a Circuit

1. **Add Components**: Select "Add Component" menu → Choose block type
2. **Configure**: Edit parameters in left panel
3. **Connect**: Add wires and set bit ranges (LSB/MSB)
4. **Generate**: Click "Generate Code" for Python simulation
5. **Save**: Export circuit as image via "File" → "Save Image"

**Pro Tips:**

- Orange wires represent clock connections
- Black wires are data connections
- Right-click blocks for quick properties access
- Use zoom slider for detailed views

## API Reference

### Core Module: `pydig`

```python
# Main simulation object
simulator = pydig.pydig(name="simulation_name")

# Create components
simulator.source(filePath, plot=False, blockID="input")
simulator.moore(maxOutSize, plot=False, blockID="fsm", nsl=None, ol=None)
simulator.clock(timePeriod, onTime, blockID="clk")
simulator.combinational(maxOutSize, func, blockID="logic", delay=0)
simulator.output(plot=False, blockID="output")

# Execute simulation
simulator.generateCSV()  # Enable CSV output
simulator.run(until=100)  # Run for 100 time units
```

### Moore Machine API

```python
# Connections
moore.input()      # Connect input signals
moore.clock()      # Connect clock signal
moore.output()     # Access output port

# Configuration
moore.nsl = func   # Set next state logic
moore.ol = func    # Set output logic

# Queries
moore.isConnected()     # Check connection status
moore.getInputVal()     # Get current input value
moore.getBlockID()      # Get block identifier
```

### Combinational Block API

```python
# Create combinational logic
comb = simulator.combinational(
    maxOutSize=8,
    func=lambda x: x ^ 0xFF,  # XOR with 0xFF
    delay=0.1,
    blockID="inverter"
)

# Use in connections
source.output() > comb.input()
comb.output() > sink.input()
```

## Project Structure

```
MooreMachine/
├── Python Components/
│   ├── pydig.py              # Main simulation manager
│   ├── blocks.py             # Core block classes
│   ├── simulation.py         # Event simulation engine
│   ├── main.py               # Entry point
│   └── BuildingBlocks/       # Pre-built components
│       ├── BasicGates.py     # Logic gates
│       ├── BitCounters.py    # Counter implementations
│       ├── Latches.py        # Latch designs
│       └── ...
├── Java Components/
│   ├── Simulator/
│   │   ├── pom.xml           # Maven build config
│   │   └── src/
│   │       ├── main/java/    # GUI source code
│   │       └── test/java/    # JUnit test suite
│   └── FiniteStateMachineSimulation.jar  # Pre-built JAR
├── Tests/                    # Test data files
├── Tester_Python/            # Python integration tests
├── Images/                   # Documentation images
├── requirements.txt          # Python dependencies
└── README.md
```

## Testing

### Python Test Suite

```bash
cd Tester_Python

# Unit tests
python -m pytest Unit\ Testing/

# Module tests
python -m pytest Module\ Testing/

# Integration tests
python -m pytest Integration\ Testing/
```

### Java Tests

```bash
cd Simulator
mvn test                    # Run all tests
mvn test -Dtest=ClockTest  # Run specific test
```

## Advanced Features

### Custom Connection Syntax

```python
# Connect bits 0-4 from block1 to block2
block1.output(0, 4) > block2.input()

# Connect all bits
block1.output() > block2.input()

# Chain connections
source.output() > gate1.input() > gate2.input() > output.input()

# Multiple inputs (concatenation)
block1.output(0, 2) > combined.input()  # Bits 0-2 as LSB
block2.output(0, 2) > combined.input()  # Bits 0-2 as MSB
```

### PWM Signal Generation

```python
def pwm_nsl(state, input_val):
    """Mod-4 counter next state"""
    return (state + 1) & 0x3 if input_val else state

def pwm_ol(state):
    """Output current count"""
    return state

# Create PWM simulator...
counter = simulator.moore(maxOutSize=2, blockID="PWM_Counter")
counter.nsl = pwm_nsl
counter.ol = pwm_ol
```

### File I/O Operations

```python
# Read from CSV input file
input_block = simulator.source(
    filePath="signals/input.csv",
    plot=True,          # Display input waveform
    blockID="Input1"
)

# Generate simulation output
simulator.generateCSV()
simulator.run(until=1000)

# Output stored in: <simulation_name>.csv
```

## Performance Considerations

| Aspect                  | Recommendation                                    |
| ----------------------- | ------------------------------------------------- |
| **Simulation Duration** | Keep < 10,000 time units for fast execution       |
| **Block Count**         | 50-100 blocks optimal; 200+ may be slow           |
| **Data Points**         | 1,000-10,000 points for clear visualizations      |
| **File Format**         | CSV for best compatibility; XLSX for spreadsheets |

## Troubleshooting

### Common Issues & Solutions

#### Python Import Errors

```bash
# Reinstall all dependencies
pip install --upgrade --force-reinstall -r requirements.txt
```

#### GUI Won't Start

```bash
# Verify Java installation
java -version

# Run with verbose output
java -jar FiniteStateMachineSimulation.jar -v
```

#### CSV Not Generated

```python
# IMPORTANT: Call generateCSV() BEFORE run()
simulator.generateCSV()
simulator.run(until=100)  # Correct order

# CSV will be saved as: <name>.csv in output/ directory
```

#### Moore Machine Not Connected

```python
# Check all ports are connected
if not moore.isConnected():
    print("Missing connections!")
    print(f"Input connected: {moore.getInputCount() > 0}")
```

## Contributing

We welcome contributions! Please follow these guidelines:

### Getting Started

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Implement** your changes with tests
4. **Commit** with clear messages: `git commit -m 'Add amazing feature'`
5. **Push** to your branch: `git push origin feature/amazing-feature`
6. **Submit** a Pull Request

### Code Standards

- **Python**: PEP 8 ([style guide](https://www.python.org/dev/peps/pep-0008/))
- **Java**: [Google Java Style Guide](https://google.github.io/styleguide/javaguide.html)
- Include docstrings and comments for complex logic
- Write tests for new features
- Ensure backward compatibility

### Pull Request Checklist

- [ ] Code follows project style guidelines
- [ ] All tests pass locally
- [ ] Documentation updated
- [ ] No breaking changes introduced
- [ ] Clear description of changes

## Citation

If you use this simulator in academic or research work, please cite:

```bibtex
@software{mooremachine2025,
  title={Moore Machine Simulator: Python and Java Implementation},
  author={Jindal, Gathik},
  year={2025},
  url={https://github.com/gathik-jindal/MooreMachine},
  note={Accessed: 2025-06-15}
}
```

## License

This project is licensed under the **MIT License** - see [LICENSE](LICENSE) file for complete terms.

**Copyright © 2025 Gathik Jindal**

Permission is hereby granted to use, modify, and distribute this software for both commercial and non-commercial purposes, subject to the conditions in the LICENSE file.

## Support & Resources

| Resource             | Link                                                                            |
| -------------------- | ------------------------------------------------------------------------------- |
| 📚 **Documentation** | [GitHub Wiki](https://github.com/gathik-jindal/MooreMachine/wiki)               |
| 🐛 **Bug Reports**   | [GitHub Issues](https://github.com/gathik-jindal/MooreMachine/issues)           |
| 💬 **Discussion**    | [GitHub Discussions](https://github.com/gathik-jindal/MooreMachine/discussions) |
| 📧 **Contact**       | gathik.jindal@example.com                                                       |

## Acknowledgments

- **Moore Machine Theory**: Edward F. Moore's foundational work on finite state machines
- **SimPy**: The excellent discrete event simulation framework
- **Community**: All contributors, testers, and users

## Roadmap

### Planned Features

- [ ] Support for Mealy Machines
- [ ] VHDL code generation
- [ ] Network-based simulation coordination
- [ ] WebGL-based browser visualization
- [ ] Multi-threaded simulation for large designs
- [ ] Integration with HDL simulators

### Recent Updates

- ✅ Java GUI with drag-and-drop interface
- ✅ Multi-format input file support
- ✅ Comprehensive building block library
- ✅ CSV output generation
- ✅ Real-time plotting

---

<div align="center">

### ⭐ If this project helped you, please consider giving it a star! ⭐

**[Back to Top](#moore-machine-simulator)**

Made with ❤️ by the Moore Machine community

</div>

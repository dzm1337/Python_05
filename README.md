
# Code Nexus - Data Processing Pipeline

## Overview

The **Code Nexus Data Processing Pipeline** is a polymorphic data processing system that demonstrates object-oriented programming principles, abstract base classes, and duck typing. The system processes different types of data (numeric, text, and log entries) through specialized processors and exports the results in CSV or JSON format.

## Features

- **Polymorphic Data Processing**: Common interface for different data types
- **Abstract Base Classes**: Enforces implementation of required methods
- **Duck Typing Export System**: Plugin-based export system using Protocol
- **FIFO Data Extraction**: First-In-First-Out order for data retrieval
- **Statistics Tracking**: Track processed and remaining items per processor
- **Multiple Export Formats**: CSV and JSON export plugins

## Architecture

### Class Hierarchy
DataProcessor (ABC)
├── NumericProcessor
├── TextProcessor
└── LogProcessor

DataStream
├── register_processor()
├── process_stream()
├── output_pipeline()
└── print_processors_stats()

ExportPlugin (Protocol)
├── CSVExportPlugin
└── JSONExportPlugin

text

### Components

| Class | Responsibility |
|-------|----------------|
| `DataProcessor` | Abstract base class defining the processor interface |
| `NumericProcessor` | Processes integers, floats, and lists of numbers |
| `TextProcessor` | Processes strings and lists of strings |
| `LogProcessor` | Processes dictionaries with string key-value pairs |
| `DataStream` | Routes data to appropriate processors and manages pipeline |
| `CSVExportPlugin` | Exports data as comma-separated values |
| `JSONExportPlugin` | Exports data as JSON format |

## Requirements

- Python 3.10 or higher
- No external dependencies (only standard library)

## Installation

```bash
# Clone the repository (if applicable)
git clone <repository-url>
cd code-nexus

# No installation required - just run the script
python3 data_pipeline.py
Usage
Basic Example
python
from data_pipeline import DataStream, NumericProcessor, TextProcessor, LogProcessor

# Create data stream
stream = DataStream()

# Register processors
stream.register_processor(NumericProcessor())
stream.register_processor(TextProcessor())
stream.register_processor(LogProcessor())

# Process data
data = [42, "Hello", {"key": "value"}]
stream.process_stream(data)

# Export results
csv_plugin = CSVExportPlugin()
stream.output_pipeline(3, csv_plugin)
Data Types Accepted
Processor	Accepts
Numeric	int, float, list[int], list[float], list[int | float]
Text	str, list[str]
Log	dict[str, str], list[dict[str, str]]
Export Formats
CSV Format (values only):

text
CSV Output:
3.14,-1,2.71
JSON Format (preserves rank):

text
JSON Output:
{"item_0": "3.14", "item_1": "-1", "item_2": "2.71"}
Testing
Run the built-in test scenario:

bash
python3 data_pipeline.py
Expected output demonstrates:

Registration of processors

Processing of mixed data types

Statistics tracking

CSV and JSON exports

Design Patterns
Pattern	Implementation
Abstract Base Class	DataProcessor defines interface
Template Method	output() method in base class
Strategy	Export plugins with common Protocol
Duck Typing	Export plugins without inheritance
FIFO Queue	Index-based extraction without pop(0)
Error Handling
Invalid Data: Raises exception if validate() fails before ingest()

No Processor: Prints error message if no processor can handle element

Ingestion Error: Catches exceptions during processing

Key Concepts Demonstrated
Polymorphism
The DataStream class doesn't need to know the specific type of each processor - it just calls validate() and ingest().

Duck Typing with Protocol
Export plugins don't need to inherit from any base class - they just need to implement process_output():

python
class MyCustomPlugin:
    def process_output(self, data: list[tuple[int, str]]) -> None:
        # Custom export logic
        pass
FIFO with Index Pointer
Instead of using pop(0) (inefficient) or deque (not allowed), we use an index pointer:

python
self.nxt_output_index  # Points to next item to extract
File Structure
text
ex2/
├── data_pipeline.py    # Main implementation
└── README.md           # This file
Authorized Imports
abc - Abstract Base Classes

typing - Type hints (Union, Any, Sequence, Protocol)

Built-in types (int, str, list, dict, tuple)

Constraints Satisfied
Python 3.10+ syntax

No external imports beyond abc and typing

Comprehensive type annotations (mypy compatible)

Flake8 compliant (max 79 characters per line)

Exception handling for data integrity

Duck typing for export plugins

Example Output
text
=== Code Nexus - Data Pipeline ===
Initialize Data Stream...
No processor found, no data
Registering Processors

Send first batch of data on stream: ['Hello world', [4.14, -1, 2.71], ...]

== DataStream statistics ==
NumericProcessor: total 4 items processed, remaining 4 on processor
TextProcessor: total 3 items processed, remaining 3 on processor
LogProcessor: total 2 items processed, remaining 2 on processor

Send 3 processed data from each processor to a CSV plugin:
CSV Output:
4.14,-1,2.71
CSV Output:
Hello world,Hi,five
CSV Output:
WARNING: Telnet access! Use ssh instead,INFO: User wil is connected

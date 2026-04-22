from abc import ABC, abstractmethod
from typing import Any, Sequence


class DataProcessor(ABC):
    def __init__(self) -> None:
        self.idx_counter: int = 0
        self.storage: list[tuple[int, str]] = []

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    @abstractmethod
    def ingest(self, data: Any) -> None:
        pass

    def output(self) -> tuple[int, str]:
        if self.storage:
            return self.storage.pop(0)
        return (0, "")


class NumericProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, bool):
            return False
        if isinstance(data, (int, float)):
            return True
        if isinstance(data, list) and len(data) > 0:
            return all(
                not isinstance(data, bool) and isinstance(item, (int, float))
                for item in data
            )
        return False

    def ingest(
        self, data: int | float | Sequence[int | float]
    ) -> None:
        if not self.validate(data):
            raise Exception("Improper numeric data")

        tmp_data = [data] if isinstance(data, (int, float)) else data

        for item in tmp_data:
            self.storage.append((self.idx_counter, str(item)))
            self.idx_counter += 1


class TextProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, str):
            return True
        if isinstance(data, list) and len(data) > 0:
            return all(isinstance(item, str) for item in data)
        return False

    def ingest(self, data: str | list[str]) -> None:
        if not self.validate(data):
            raise Exception("Improper text data")

        tmp_data = [data] if isinstance(data, str) else data

        for item in tmp_data:
            self.storage.append((self.idx_counter, item))
            self.idx_counter += 1


class LogProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, dict) and len(data) > 0:
            return all(
                isinstance(k, str) and isinstance(v, str)
                for k, v in data.items()
            )
        if isinstance(data, list) and len(data) > 0:
            return all(
                isinstance(item, dict)
                and all(
                    isinstance(k, str) and isinstance(v, str)
                    for k, v in item.items()
                )
                for item in data
            )
        return False

    def ingest(self, data: dict[str, str] | list[dict[str, str]]) -> None:
        if not self.validate(data):
            raise Exception("Improper log data")

        tmp_data = [data] if isinstance(data, dict) else data

        for log_dict in tmp_data:
            if "log_level" in log_dict and "log_message" in log_dict:
                log_str = f"{log_dict['log_level']}: {log_dict['log_message']}"
            else:
                parts = []
                for k, v in log_dict.items():
                    parts.append(f"{k}: {v}")
                log_str = ", ".join(parts)
            self.storage.append((self.idx_counter, log_str))
            self.idx_counter += 1


if __name__ == "__main__":
    print("=== Code Nexus - Data Processor ===")

    nproc = NumericProcessor()
    tproc = TextProcessor()
    lproc = LogProcessor()

    print("Testing Numeric Processor...")
    print(f"Trying to validate input '42': {nproc.validate(42)}")
    print(f"Trying to validate input 'Hello': {nproc.validate('Hello')}")
    print(
        "Test with invalid ingestion of string 'foo' without prior validation:"
    )

    try:
        nproc.ingest("foo")
    except Exception as e:
        print(f"Got exception: {e}")

    valid_num_input = [1, 2, 3, 4, 5]
    print(f"Processing data: {valid_num_input}")
    nproc.ingest(valid_num_input)

    print("Extracting 3 values...")
    for _ in range(3):
        idx, val = nproc.output()
        print(f"Numeric value {idx}: {val}")

    print("\nTesting Text Processor...")
    print(f"Trying to validate input '42': {tproc.validate('42')}")
    tproc.ingest(["Hello", "Nexus", "World"])
    print("Processing data: ['Hello', 'Nexus', 'World']")
    print("Extracting 1 value...")
    idx, val = tproc.output()
    print(f"Text value {idx}: {val}")

    print("\nTesting Log Processor...")
    print(f"Trying to validate input 'Hello': {lproc.validate('Hello')}")
    log_data = [
        {"log_level": "NOTICE", "log_message": "Connection to server"},
        {"log_level": "ERROR", "log_message": "Unauthorized access!!"},
    ]
    lproc.ingest(log_data)
    print(f"Processing data: {log_data}")
    print("Extracting 2 values...")
    for _ in range(2):
        idx, val = lproc.output()
        print(f"Log entry {idx}: {val}")

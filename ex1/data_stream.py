from abc import ABC, abstractmethod
from typing import Union, Any


class DataProcessor(ABC):

    def __init__(self):
        self.idx_counter = 0
        self.nxt_output_index = 0
        self.storage = []
        self.processed_count = 0

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    @abstractmethod
    def ingest(self, data: Any) -> None:
        pass

    def output(self) -> tuple[int, str]:
        if self.nxt_output_index < len(self.storage):
            idx, output = self.storage[self.nxt_output_index]
            self.nxt_output_index += 1
            return (idx, output)
        return (0, "")

    def get_processed_count(self) -> int:
        return self.processed_count

    def get_remaining_count(self) -> int:
        return len(self.storage) - self.nxt_output_index


class NumericProcessor(DataProcessor):

    def validate(self, data: Any) -> bool:
        if isinstance(data, (int, float)):
            return True
        if isinstance(data, list):
            return all(isinstance(item, (int, float)) for item in data)
        return False

    def ingest(self, data: Union[int, float, list[Union[int, float]]]) -> None:
        if not self.validate(data):
            raise Exception("Improper numeric data")

        if isinstance(data, (int, float)):
            tmp_data = [data]
        else:
            tmp_data = data

        for item in tmp_data:
            self.storage.append((self.idx_counter, str(item)))
            self.idx_counter += 1
            self.processed_count += 1


class TextProcessor(DataProcessor):

    def validate(self, data: Any) -> bool:
        if isinstance(data, str):
            return True
        if isinstance(data, list):
            return all(isinstance(item, str) for item in data)
        return False

    def ingest(self, data: Union[str, list[str]]) -> None:
        if not self.validate(data):
            raise Exception("Improper text data")

        if isinstance(data, str):
            tmp_data = [data]
        else:
            tmp_data = data

        for item in tmp_data:
            self.storage.append((self.idx_counter, item))
            self.idx_counter += 1
            self.processed_count += 1


class LogProcessor(DataProcessor):

    def validate(self, data: Any) -> bool:
        if isinstance(data, dict):
            return all(isinstance(k, str) and isinstance(v, str)
                       for k, v in data.items())
        if isinstance(data, list):
            return all(
                isinstance(item, dict) and
                all(isinstance(k, str) and isinstance(v, str)
                    for k, v in item.items())
                for item in data
            )
        return False

    def ingest(
        self,
        data: Union[dict[str, str], list[dict[str, str]]]
    ) -> None:
        if not self.validate(data):
            raise Exception("Improper log data")

        if isinstance(data, dict):
            tmp_data = [data]
        else:
            tmp_data = data

        for log_dict in tmp_data:
            if 'log_level' in log_dict and 'log_message' in log_dict:
                log_str = f"{log_dict['log_level']}: {log_dict['log_message']}"
            else:
                parts = []
                for k, v in log_dict.items():
                    parts.append(f"{k}: {v}")
                log_str = ", ".join(parts)
            self.storage.append((self.idx_counter, log_str))
            self.idx_counter += 1
            self.processed_count += 1


class DataStream:
    def __init__(self):
        self.processors = []

    def register_processor(self, proc: DataProcessor) -> None:
        self.processors.append(proc)

    def process_stream(self, stream: list[Any]) -> None:
        for element in stream:
            processed = False
            for processor in self.processors:
                if processor.validate(element):
                    try:
                        processor.ingest(element)
                        processed = True
                        break
                    except Exception:
                        print(f"DataStream error - Error ingesting element: "
                              f"{element}")
                        processed = True
                        break
            if not processed:
                print(f"DataStream error - Can't process element in stream: "
                      f"{element}")

    def print_processors_stats(self) -> None:
        if not self.processors:
            print("No processor found, no data")
            return

        for processor in self.processors:
            processor_name = processor.__class__.__name__
            total = processor.get_processed_count()
            remaining = processor.get_remaining_count()
            print(f"{processor_name}: total {total} items processed, "
                  f"remaining {remaining} on processor")


if __name__ == "__main__":
    print("=== Code Nexus - Data Stream ===")

    print("Initialize Data Stream...")
    data_stream = DataStream()

    data_stream.print_processors_stats()

    print("Registering Numeric Processor")
    num_proc = NumericProcessor()
    data_stream.register_processor(num_proc)

    first_batch = [
        'Hello world',
        [3.14, -1, 2.71],
        [{'log_level': 'WARNING',
          'log_message': 'Telnet access! Use ssh instead'},
         {'log_level': 'INFO',
          'log_message': 'User wil is connected'}],
        42,
        ['Hi', 'five']
    ]
    print("Send first batch of data on stream:", first_batch)
    data_stream.process_stream(first_batch)

    print("== DataStream statistics ==")
    data_stream.print_processors_stats()

    print("\nRegistering other data processors")
    text_proc = TextProcessor()
    log_proc = LogProcessor()
    data_stream.register_processor(text_proc)
    data_stream.register_processor(log_proc)

    print("Send the same batch again")
    data_stream.process_stream(first_batch)

    print("== DataStream statistics ==")
    data_stream.print_processors_stats()

    print("\nConsume some elements from the data processors: "
          "Numeric 3, Text 2, Log 1")
    for _ in range(3):
        num_proc.output()
    for _ in range(2):
        text_proc.output()
    for _ in range(1):
        log_proc.output()

    print("== DataStream statistics ==")
    data_stream.print_processors_stats()

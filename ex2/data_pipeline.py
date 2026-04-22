from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import Any, Protocol


class DataProcessor(ABC):
    def __init__(self) -> None:
        self.idx_counter: int = 0
        self.storage: list[tuple[int, str]] = []
        self.processed_count: int = 0

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

    def get_processed_count(self) -> int:
        return self.processed_count

    def get_remaining_count(self) -> int:
        return len(self.storage)


class NumericProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, bool):
            return False
        if isinstance(data, (int, float)):
            return True
        if isinstance(data, list) and len(data) > 0:
            return all(
                not isinstance(item, bool) and isinstance(item, (int, float))
                for item in data
            )
        return False

    def ingest(self, data: int | float | Sequence[int | float]) -> None:
        if not self.validate(data):
            raise Exception("Improper numeric data")

        tmp_data = [data] if isinstance(data, (int, float)) else data

        for item in tmp_data:
            self.storage.append((self.idx_counter, str(item)))
            self.idx_counter += 1
            self.processed_count += 1


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
            self.processed_count += 1


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
            self.processed_count += 1


class ExportPlugin(Protocol):
    def process_output(self, data: list[tuple[int, str]]) -> None: ...


class CSVExportPlugin:
    def process_output(self, data: list[tuple[int, str]]) -> None:
        if not data:
            return
        values = [str(item[1]) for item in data]
        print("CSV Output:")
        print(",".join(values))


class JSONExportPlugin:
    def process_output(self, data: list[tuple[int, str]]) -> None:
        if not data:
            return
        items = []
        for rank, value in data:
            items.append(f'"item_{rank}": "{value}"')
        json_str = "{" + ", ".join(items) + "}"
        print("JSON Output:")
        print(json_str)


class DataStream:
    def __init__(self) -> None:
        self.processors: list[DataProcessor] = []

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
                        print(
                            f"DataStream error - Error ingesting element: "
                            f"{element}"
                        )
                        processed = True
                        break
            if not processed:
                print(
                    f"DataStream error - Can't process element in stream: "
                    f"{element}"
                )

    def output_pipeline(self, nb: int, plugin: ExportPlugin) -> None:
        for processor in self.processors:
            data_to_export: list[tuple[int, str]] = []
            for _ in range(nb):
                if processor.get_remaining_count() == 0:
                    break
                rank, value = processor.output()
                data_to_export.append((rank, value))
            if data_to_export:
                plugin.process_output(data_to_export)

    def print_processors_stats(self) -> None:
        if not self.processors:
            print("No processor found, no data")
            return

        for processor in self.processors:
            processor_name = processor.__class__.__name__
            total = processor.get_processed_count()
            remaining = processor.get_remaining_count()
            print(
                f"{processor_name}: total {total} items processed, "
                f"remaining {remaining} on processor"
            )


if __name__ == "__main__":
    print("=== Code Nexus - Data Pipeline ===")

    print("Initialize Data Stream...")
    data_stream = DataStream()
    data_stream.print_processors_stats()

    print("Registering Processors")
    num_proc = NumericProcessor()
    text_proc = TextProcessor()
    log_proc = LogProcessor()
    data_stream.register_processor(num_proc)
    data_stream.register_processor(text_proc)
    data_stream.register_processor(log_proc)

    first_batch: list[Any] = [
        "Hello world",
        [4.14, -1, 2.71],
        [
            {
                "log_level": "WARNING",
                "log_message": "Telnet access! Use ssh instead",
            },
            {"log_level": "INFO", "log_message": "User wil is connected"},
        ],
        43,
        ["Hi", "five"],
    ]

    print(f"\nSend first batch of data on stream: {first_batch}")
    data_stream.process_stream(first_batch)

    print("\n== DataStream statistics ==")
    data_stream.print_processors_stats()

    print("Send 3 processed data from each processor to a CSV plugin:")
    csv_plugin = CSVExportPlugin()
    data_stream.output_pipeline(3, csv_plugin)

    print("\n== DataStream statistics ==")
    data_stream.print_processors_stats()

    second_batch: list[Any] = [
        22,
        ["I love AI", "LLMs are wonderful", "Stay healthy"],
        [
            {"log_level": "ERROR", "log_message": "501 server crash"},
            {
                "log_level": "NOTICE",
                "log_message": "Certificate expires in 11 days",
            },
        ],
        [33, 42, 64, 84, 128, 168],
        "World hello",
    ]

    print(f"\nSend another batch of data: {second_batch}")
    data_stream.process_stream(second_batch)

    print("\n== DataStream statistics ==")
    data_stream.print_processors_stats()

    print("Send 5 processed data from each processor to a JSON plugin:")
    json_plugin = JSONExportPlugin()
    data_stream.output_pipeline(5, json_plugin)

    print("\n== DataStream statistics ==")
    data_stream.print_processors_stats()

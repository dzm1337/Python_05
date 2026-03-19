from abc import ABC, abstractmethod

class DataProcessor(ABC):

    @abstractmethod
    def process(self, data: any) -> str:
        pass
    @abstractmethod
    def validate(self, data: any) -> bool:
        pass
    def run(self, data: any) -> None:
        pass
    def format_output(self, result: str) -> str:
        return f"Output: {result}"
    
class NumericProcessor(DataProcessor):
 
    def validate(self, data: any) -> bool:
        if type(data) is not list:
            return False
        try:
            for num in data:
                int(num)
        except ValueError:
            raise ValueError("Error: not a valid integer...")
        return True

    def process(self, data: any) -> str:
        if self.validate(data) == False:
            raise Exception(f"Error: Not valid type!")
        return f"Processed {len(data)} numeric values, sum={sum(data)}, avg={sum(data) / len(data)}"
    
    def run(self, data: any) -> None:
        print(f'Processing data: {data}')
        print("Validation: Numeric data verified")
        result = self.process(data)
        formatted = self.format_output(result)
        return formatted

class TextProcessor(DataProcessor):

    def validate(self, data: any) -> bool:
        if type(data) is not str:
                return False
        return True
    
    def count_words(self, data: any):
        i = 0
        count = 0
        while (i < len(data)):
            if (data[i] == ' '):
                i += 1
            if (i < len(data) and data[i] != ' '):
                count += 1
                while (i < len(data) and data[i] != ' '):
                    i += 1
            i += 1
        return count
    
    def process(self, data: any) -> str:
        if self.validate(data) is False:
            raise Exception(f"Error: invalid type!")
        return f"Processed text: {len(data)} characters, {self.count_words(data)} words"
    
    def run(self, data: any) -> None:
        result = self.process(data)
        formatted = self.format_output(result)
        print(f'Processing data: "{data}"')
        print("Validation: Text data verified")
        return (formatted)

class LogProcessor(DataProcessor):

    def validate(self, data: any) -> bool:
        if type(data) is not str or ":" not in data:
            return False
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        parts = data.split(":", 1)
        level = parts[0].upper()
        if level not in valid_levels:
            raise Exception("Not a valid level!")
        return True
    
    def process(self, data: any) -> str:
        if self.validate(data) == False:
            raise Exception("Error: invalid type!")
        parts = data.split(":", 1)
        level = parts[0].upper()
        if level in ["ERROR", "CRITICAL"]:
            return f"[ALERT]: {level} level detected: Connection timeout"
        elif level is "INFO":
            return f"[INFO] INFO level detected: System ready"
        else:
            return f"[{level}]: {level} level detected: Connection timeout"
        
    def run(self, data: any) -> None:
        print(f'Processing data: "{data}"')
        print("Validation: Log entry verified")
        result = self.process(data)
        formatted = self.format_output(result)
        return result
        
def processing_number(num_list):
  
    print("\nInitializing Numeric Processor...")
    processor = NumericProcessor()
    print(processor.run(num_list))
    
def processing_text(text):

    print("\nInitializing Text Processor...")
    processor = TextProcessor()
    print(processor.run(text))

    
def processing_log(log_text):

    print("\nInitializing Log Processor...")
    processor = LogProcessor()
    print(processor.run(log_text))

def multiple_types():

    print("\nProcessing multiple data types through same interface...")
    inputs = [
        [2, 2, 2],
        "Hello Nexus World",
        "INFO: level detected: System ready"
    ]
    processors = [
        NumericProcessor(),
        TextProcessor(),
        LogProcessor()
    ]
    i = 0
    while (i < len(inputs)):
            print(f"Result {i + 1}: {processors[i].process(inputs[i])}")
            i += 1
if __name__ == "__main__":
    try:
        processing_number([1, 2, 3, 4, 5])
        processing_text("Hello Nexus World")
        processing_log("ERROR:Connection timeout")
        multiple_types()
    except (Exception, ValueError) as e:
            print(e)
    print("\nFoundation systems online. Nexus ready for advanced streams.")
                
from abc import ABC, abstractmethod

class DataProcessor(ABC):

    @abstractmethod
    def process(self, data: any) -> str:
        pass
    @abstractmethod
    def validate(self, data: any) -> bool:
        pass
    @abstractmethod
    def format_output(self, result: str) -> str:
        pass

class NumericProcessor(DataProcessor):
 
    def validate(self, data: any) -> bool:
        if type(data) is not list:
            return False
        try:
            for num in data:
                int(num)
        except ValueError:
            raise ValueError("Error: not a valid integer...")
            return False
        return True

    def process(self, data: any) -> str:
        if self.validate(data) == False:
            raise Exception(f"Error: Not valid type!")
        print(f'Processing data: {data}')
        print("Validation: Numeric data verified")
    
    def format_output(self, result: list[int]) -> str:
        return f"Output: Processed {len(result)} numeric values, sum={sum(result)}, avg={sum(result) / len(result)}"

def processing_number():
    
    num_list = [1, 2, 3, 4, 5]
    num = NumericProcessor()
    num.validate(num_list)
    num.process(num_list)
     

if __name__ == "__main__":
     
    try:
        num_list = "x"
       print(num.format_output(num_list))
    except (Exception, ValueError) as e:
        print(e)
    
    

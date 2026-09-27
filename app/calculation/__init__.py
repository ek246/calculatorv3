from abc import ABC, abstractmethod
"import operations from Operations class"
from app.operations import Operations

class Calculation(ABC):
    def __init__(self, a: float, b: float) -> None:
        self.a = a # first operand
        self.b = b # second operand

    @abstractmethod
    def execute(self) -> float:
        pass #pragma: no cover
    def __str__(self) -> str:
        return self._str_()
    def _str_(self) -> str:
        """Return a string representation of the calculation performed."""
        outcome = self.execute()
        operation_performed = self.__class__.__name__
        return f"{operation_performed}({self.a}, {self.b}) = {outcome}"
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.a}, {self.b})"

class CalculationFactory:
   calc_dict = {}

   @classmethod
   def register_calculation(cls, calc_type: str):
       def decorator(calc_class: type) -> type:
           calc_type = calc_type.lower()
           if calc_type in cls.calc_dict:
               raise ValueError(f"'{calc_type}' already exists")
       
           cls.calc_dict[calc_type] = calc_class
           return calc_class
       return decorator
   @classmethod
   def create_calculation(cls, calc_type: str, a: float, b: float) -> Calculation:
       calc_type = calc_type.lower()
       if calc_type not in cls.calc_dict:
           raise ValueError(f"'{calc_type}' is unknown. The known types are: {', '.join(cls.calc_dict.keys())}")
       return cls.calc_dict[calc_type](a, b)

@CalculationFactory.register_calculation("add")
class Add(Calculation):
    def execute(self) -> float:
         return Operations.addition(self.a, self.b )

@CalculationFactory.register_calculation("subtract")
class Subtract(Calculation):
    def execute(self) -> float:
        return Operations.subtraction(self.a, self.b)

@CalculationFactory.register_calculation("multiply")
class Multiply(Calculation):
    def execute(self) -> float:
        return Operations.multiplication(self.a, self.b)

@CalculationFactory.register_calculation("divide")
class Divide(Calculation):
    def execute(self) -> float:
        if self.b == 0:
                    raise ZeroDivisionError("You cannot divide by zero.")
        return Operations.division(self.a, self.b)


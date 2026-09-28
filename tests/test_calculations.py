import pytest
from unittest.mock import patch
from app.operations import Operations
from app.calculation import (
    CalculationFactory,
    Calculation,
    Add,
    Subtract,
    Multiply,
    Divide,
)
@patch.object(Operations, "addition")
def test_add_positive(mock_add):
    a = 2
    b = 3
    expected_result = 5
    mock_add.return_value = expected_result
    add_calc = Add(a, b)

    result = add_calc.execute()

    mock_add.assert_called_once_with(a, b)
    assert result == expected_result

@patch.object(Operations, "addition")
def test_add_negative(mock_add):
    a = 2
    b = 3
    mock_add.side_effect = Exception("Addition failed")
    add_calc = Add(a, b)

    with pytest.raises(Exception) as exc_info:
        add_calc.execute()
    assert str(exc_info.value) == "Addition failed"

@patch.object(Operations, "subtraction")
def test_subtract_positive(mock_subtract):
    a = 5
    b = 3
    expected_result = 2
    mock_subtract.return_value = expected_result
    subtract_calc = Subtract(a, b)

    result = subtract_calc.execute()

    mock_subtract.assert_called_once_with(a, b)
    assert result == expected_result

@patch.object(Operations, "subtraction")
def test_subtract_negative(mock_subtract):
    a = 5
    b = 3
    mock_subtract.side_effect = Exception("Subtraction failed")
    subtract_calc = Subtract(a, b)

    with pytest.raises(Exception) as exc_info:
        subtract_calc.execute()
    assert str(exc_info.value) == "Subtraction failed"

@patch.object(Operations, "multiplication")
def test_multiply_positive(mock_multiply):
    a = 2
    b = 3
    expected_result = 6
    mock_multiply.return_value = expected_result
    multiply_calc = Multiply(a, b)

    result = multiply_calc.execute()

    mock_multiply.assert_called_once_with(a, b)
    assert result == expected_result

@patch.object(Operations, "multiplication")
def test_multiply_negative(mock_multiply):
    a = 2
    b = 3
    mock_multiply.side_effect = Exception("Multiplication failed")
    multiply_calc = Multiply(a, b)

    with pytest.raises(Exception) as exc_info:
        multiply_calc.execute()
    assert str(exc_info.value) == "Multiplication failed"

@patch.object(Operations, "division")
def test_divide_positive(mock_divide):
    a = 6
    b = 3
    expected_result = 2
    mock_divide.return_value = expected_result
    divide_calc = Divide(a, b)

    result = divide_calc.execute()

    mock_divide.assert_called_once_with(a, b)
    assert result == expected_result

@patch.object(Operations, "division")
def test_divide_negative(mock_divide):
    a = 6
    b = 3
    mock_divide.side_effect = Exception("Division failed")
    divide_calc = Divide(a, b)

    with pytest.raises(Exception) as exc_info:
        divide_calc.execute()
    assert str(exc_info.value) == "Division failed"

@patch.object(Operations, "division")
def test_divide_by_zero(mock_divide):
    a = 1
    b = 0
    divide_calc = Divide(a, b)

    with pytest.raises(ZeroDivisionError) as exc_info:
        divide_calc.execute()
    
    assert str(exc_info.value) == "You cannot divide by zero."

   
def test_factory_create_add():
    a = 3
    b = 2

    calc = CalculationFactory.create_calculation("addition", a, b)

    assert isinstance(calc, Add)
    assert calc.a == a
    assert calc.b == b
def test_factory_create_subtract():
    a = 3
    b = 2

    calc = CalculationFactory.create_calculation("subtraction", a, b)

    assert isinstance(calc, Subtract)
    assert calc.a == a
    assert calc.b == b

def test_factory_create_multiply():
    a = 3
    b = 2

    calc = CalculationFactory.create_calculation("multiplication", a, b)

    assert isinstance(calc, Multiply)
    assert calc.a == a
    assert calc.b == b

def test_factory_create_divide():
    a = 6
    b = 3

    calc = CalculationFactory.create_calculation("division", a, b)

    assert isinstance(calc, Divide)
    assert calc.a == a
    assert calc.b == b
def test_factory_register_calculation_duplication():
    with pytest.raises(ValueError) as exc_info:
        @CalculationFactory.register_calculation("addition")
        class AnotherAdd(Calculation):
            def execute(self) -> float:
                return Operations.addition(self.a, self.b)
    assert str(exc_info.value) == "'addition' already exists"
def test_factory_create_unknown_calculation():
    a = 3
    b = 2
    unknown = 'modulus'

    with pytest.raises(ValueError) as exc_info:
        CalculationFactory.create_calculation(unknown, a, b)
    assert f"'{unknown}' is unknown. The known types are: addition, subtraction, multiplication, division" == str(exc_info.value)

@patch.object(Operations, 'addition', return_value=5)
def test_calculation_str_representation_add(mock_add):
    a = 3
    b = 2
    add_calc = Add(a, b)
    result_str = str(add_calc)
    assert result_str == "Add(3, 2) = 5"

@patch.object(Operations, 'subtraction', return_value=1)
def test_calculation_str_representation_subtract(mock_sub):
    a = 3
    b = 2
    sub_calc = Subtract(a, b)
    result_str = str(sub_calc)
    assert result_str == "Subtract(3, 2) = 1"

@patch.object(Operations, 'multiplication', return_value=6)
def test_calculation_str_representation_multiply(mock_multiply):
    a = 3
    b = 2
    mul_calc = Multiply(a, b)
    result_str = str(mul_calc)
    assert result_str == "Multiply(3, 2) = 6"

@patch.object(Operations, 'division', return_value=2)
def test_calculation_str_representation_divide(mock_divide):
    a = 6
    b = 3
    div_calc = Divide(a, b)
    result_str = str(div_calc)
    assert result_str == "Divide(6, 3) = 2"

@pytest.mark.parametrize("operation, a, b, expected", [
    ("addition", 3, 2,  5),
    ("subtraction", 3, 2, 1),
    ("multiplication", 3, 2, 6),
    ("division", 6, 3, 2),
])
def test_calculation_execute(operation, a, b, expected):
    calc = CalculationFactory.create_calculation(operation, a, b)
    result = calc.execute()
    assert result == expected
def test_calc_repr():
    a = 3
    b = 2
    add_calc = Add(a, b)
    assert repr(add_calc) == "Add(3, 2)"
    
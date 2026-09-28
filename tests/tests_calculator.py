""" tests/test_calculator.py """
import sys, pytest
from io import StringIO
from app.calculator import calculator, help, history


# Helper function to display help message
def help_test(capsys):
    help()
    captured_output = capsys.readouterr()
    correct_output = """
    How to use the calculator:
    - To perform a calculation, enter an operation followed by two numbers (e.g., 'add 2 3').
    -Supported operations: addition, subtraction, multiplication, division
    -addition: adds two numbers
    -subtraction: subtracts the second number from the first
    -multiplication: multiplies two numbers
    -division: divides the first number by the second
Other commands:
    -help: displays this help message
    -history: displays the preformed calculations
    -stop: exits the calculator
Examples:
    -add 2 3
    -subtract 5 1
    -multiply 4 3
    -divide 10 2
"""
    assert captured_output.out.strip() == correct_output.strip()

def test_empty_history(capsys):
    test_history = []

    history(test_history)
    captured = capsys.readouterr()
    assert captured.out.strip() == "You have not done any calculations yet."

def test_full_history(capsys):
    test_history = ["add 2 3", "subtract 5 1"]

    history(test_history)
    captured = capsys.readouterr()
    assert "add 2 3" in captured.out.strip()
    assert "subtract 5 1" in captured.out.strip()

def test_calculator_shutdown(monkeypatch):
    inputs = ["stop"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "Stopping the calculator." in output

def test_calculator_help(monkeypatch):
    user_input = ["help", "stop"]
    output = run_calculator_with_input(monkeypatch, user_input)
    assert "How to use the calculator:" in output
    assert "Stopping the calculator." in output

def run_calculator_with_input(monkeypatch, inputs):
    """
    Simulates user input and captures output from the calculator REPL.
    
    :param monkeypatch: pytest fixture to simulate user input
    :param inputs: list of inputs to simulate
    :return: captured output as a string
    """
    input_iterator = iter(inputs)
    monkeypatch.setattr('builtins.input', lambda _: next(input_iterator))

    # Capture the output of the calculator
    captured_output = StringIO()
    sys.stdout = captured_output
    calculator()
    sys.stdout = sys.__stdout__  # Reset stdout
    return captured_output.getvalue()


# Positive Tests
def test_addition(monkeypatch):
    """Test addition operation in REPL."""
    inputs = ["add 2 3", "stop"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "The result is: 5.0" in output


def test_subtraction(monkeypatch):
    """Test subtraction operation in REPL."""
    inputs = ["subtract 5 2", "stop"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "The result is: 3.0" in output


def test_multiplication(monkeypatch):
    """Test multiplication operation in REPL."""
    inputs = ["multiply 4 5", "stop"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "The result is: 20.0" in output


def test_division(monkeypatch):
    """Test division operation in REPL."""
    inputs = ["divide 10 2", "stop"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "The result is: 5.0" in output


# Negative Tests
def test_invalid_operation(monkeypatch):
    """Test invalid operation in REPL."""
    inputs = ["modulus 5 3", "stop"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "This operation is not supported." in output
    assert "Type help to see the supported operations." in output


def test_invalid_input_format(monkeypatch):
    """Test invalid input format in REPL."""
    inputs = ["add two three", "stop"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "Invalid input. Enter two numbers and an operation." in output
    assert "For examples, type 'help" in output


def test_division_by_zero(monkeypatch):
    """Test division by zero in REPL."""
    inputs = ["divide 5 0", "stop"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "Error: You cannot divide by zero." in output

def test_calculator_display_history(monkeypatch, capsys):
    """Test displaying history in REPL."""
    user_input = 'add 2 3\nsubtract 3 2\nhistory\nstop'
    monkeypatch.setattr('sys.stdin', StringIO(user_input))
    with pytest.raises(SystemExit):
        calculator()
    captured = capsys.readouterr()
    assert "Preformed calculations:" in captured.out

def test_calculator_keyboard_interrupt(monkeypatch, capsys):
    """Test handling of keyboard interrupt (Ctrl+C) in REPL."""
    user_input = 'add 3 3\n'  # Simulate user input before sending KeyboardInterrupt
    monkeypatch.setattr('sys.stdin', StringIO(user_input))
    with pytest.raises(SystemExit):
        calculator()
    captured = capsys.readouterr()
    assert "Ctrl+C pressed. Stopping the calculator." in captured.out

def test_calculator_EOFError(monkeypatch, capsys):
    """Testing how calculator handles a EOFError (End Of File) in REPL."""
    user_input = 'add 2 3\n'  # Simulate user input before sending EOFError
    monkeypatch.setattr('sys.stdin', StringIO(user_input))
    with pytest.raises(SystemExit):
        calculator()
    captured = capsys.readouterr()
    assert "End of file reached. Stopping the calculator." in captured.out

def test_calculator_unexpected_error(monkeypatch, capsys):
    """Test handling of unexpected errors in REPL."""
    user_input = 'add 2 3\n'  # Simulate user input before sending an unexpected error
    monkeypatch.setattr('sys.stdin', StringIO(user_input))
    with pytest.raises(SystemExit):
        calculator()
    captured = capsys.readouterr()
    assert "An unexpected error occurred. Stopping the calculator." in captured.out
    
    



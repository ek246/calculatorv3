from app.calculation import CalculationFactory, Calculation
from typing import List
import sys
import readline
def help() -> None:
    instructions = """
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
    print(instructions)

def history(inputs: list[Calculation]) -> None:
    if not inputs:
        print("You have not done any calculations yet.")
    else:
        print("Preformed calculations:")
        for idx, calculation in enumerate(inputs, start=1):
            print(f"{idx}. {calculation}")


def calculator() -> None:
    inputs: list[Calculation] = []
    print("Welcome to the REPL calculator. To quit, type 'stop'.")
    print("For instructions, type 'help'. To view a history of your calculations, type 'history'.")

    
    while True:
        try:
            user_input = input("Enter an operation (e.g., 'add 2 3'), enter stop to quit: ")
            if not user_input:
                continue
            elif user_input.lower() == 'help':
                 help()
                 continue
            elif user_input.lower() == 'history':
                 history(inputs)
                 continue
            elif user_input.lower() == 'stop':
                 print("Stopping the calculator")
                 sys.exit(0)
            try:
                operation, num1, num2 = user_input.split()
                num1, num2 = float(num1), float(num2)
            except ValueError:
                print("Invalid input. Enter an operation, then two numbers")
                print("For examples, type 'help'")
                continue

            try:
                calculation = CalculationFactory.create_calculation(operation, num1, num2)
            except ValueError:
                 print("This operation is not supported.")
                 print("Type help to see the supported operations.")
                 continue
            try:
                outcome=calculation.execute()
            except ZeroDivisionError:
                print("You cannot divide by zero.")
            except Exception as e:
                print(f"An error occurred: {e}")
                print("Try again.")
                continue
            outcome_str: str = f"{calculation}"
            print(f"Result: {outcome_str}\n")

            
            inputs.append(calculation)
            print("Calculation added to history.")

        except KeyboardInterrupt:
             print("\n Ctr+C pressed. Stopping the calculator.")
             sys.exit(0) 
        except EOFError:
             print("\nCtrl+D pressed. Stopping the calculator.")
             sys.exit(0)
            


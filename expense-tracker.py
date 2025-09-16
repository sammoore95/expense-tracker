import json
from decimal import Decimal, InvalidOperation

def check_for_decimal(promt):
    """Validates user input is a decimal"""
    while True:
        user_input = input(promt)
        try:
            amount = Decimal(user_input).quantize(Decimal("0.01"))  # rounds value to a fixed number of decimal places
            return amount   
        except InvalidOperation:    # runs with Decimal operation cannot be performed
            print("Please enter a valid decimal ($) ")


def check_for_int(promt):
    """Validates user input is a whole number"""
    while True:
        user_input = input(promt)
        try:
            value = int(user_input)     # validates user input is an integer
            if value > 0:               # runs if user input is a positive whole number
                return value
            else:
                print("Please enter a whole number greater than 0")
        except ValueError:              # runs if user input is not an int
            print("Invalid input. Please enter a whole number")
    

def load_settings():
    """Loads expense tracker settings"""
    with open("settings.json", "r") as f:
        expense_settings = json.load(f)
        return(expense_settings)
    

def get_categories():
    """Returns expense categories"""
    expense_settings = load_settings()
    return expense_settings["categories"]
    

def add_expense():
    expense_name = input("Enter expense name: ")
    expense_amount = check_for_decimal("Enter amount ($)")
    get_categories()
    expense_category = check_for_int("Enter an expense category (number): ")
    # need to complete function, still needs to return expense json string, and validate proper category





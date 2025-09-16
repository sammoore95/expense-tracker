import json
from decimal import Decimal, InvalidOperation

def check_for_decimal(promt):
    """Validates user input is a decimal, returns decimal"""
    while True:
        user_input = input(promt)
        try:
            amount = Decimal(user_input).quantize(Decimal("0.01"))  # rounds value to a fixed number of decimal places
            return amount   
        except InvalidOperation:    # runs with Decimal operation cannot be performed
            print("Please enter a valid decimal ($) ")


def check_for_int(promt):
    """Validates user input is a whole number, returns int"""
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
    """Loads and returns expense tracker settings"""
    with open("settings.json", "r") as f:
        expense_settings = json.load(f)
        return(expense_settings)
    

def get_categories():
    """Returns expense categories"""
    expense_settings = load_settings()
    return expense_settings["categories"]

def validate_category_selection():
    """Validates user input is a number in the category list, returns category selection (int)"""
    expense_categories = get_categories()
    num_of_categories = (len(expense_categories))

    while True:
        user_input = check_for_int("Enter an expense category (number): ")  # uses helper function to validate user input is an int
        if user_input <= num_of_categories:     # validates user input is not an int outside of the list
            return user_input
        else:
            print("Please enter a valid category number")

    
def add_expense():
    expense_name = input("Enter expense name: ")
    expense_amount = check_for_decimal("Enter amount ($)")
    get_categories()
    expense_category = validate_category_selection()
    # need to complete function, still needs to return expense json string, and validate proper category




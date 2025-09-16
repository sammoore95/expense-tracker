import json
import uuid
from datetime import date
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


def select_category(input):
    """Selects correct category"""
    expense_categories = get_categories()
    return expense_categories[input-1]  # translates user input into selection


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


def upload_expense(expense):
    try:
        with open("expenses.json", "r") as f:
            expense_list = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        expense_list = []

    expense_list.append(expense)

    with open("expenses.json", "w") as f:
        json.dump(expense_list, f, indent=4)
        
 
def add_expense():
    """Adds expense to expenses.json file, and updates budget"""
    expense_name = input("Enter expense name: ")
    expense_amount = float(check_for_decimal("Enter amount ($): "))
    print(get_categories()) #need to still print category numbers
    expense_category = validate_category_selection()
    category_selection = select_category(expense_category)
    merchant = input("Enter Merchant: ")
    note = input("Enter Note: ")
    today = date.today()
    formated_date = today.strftime("%Y-%m-%d")

    expense_dict =  {"id":expense_name, 
                     "date":formated_date, 
                     "amount":expense_amount, 
                     "category":category_selection, 
                     "merchant":merchant, 
                     "note":note}
    

    



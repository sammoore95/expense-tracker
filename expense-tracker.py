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


def add_category():
    """Adds new category to expense categories list"""
    expense_settings = load_settings()  # loads all expense settings

    expense_categories = expense_settings["categories"]     # creates list of current expense categories

    new_category = input("What expense category would you like to add? ")

    expense_categories.append(new_category)     # appends new category to list of current expense categories

    expense_settings["categories"] = expense_categories     # applies updated categories list to the categories key in the current expense settings

    # updates settings.json file with new list of categories
    with open("settings.json", "w") as f:
        json.dump(expense_settings, f, indent=4)


def show_categories():
    """Prints categories and translates category indexes to inputs that will be intuitive for the user"""
    expense_categories = get_categories()

    print("Expense categories:")
    for i in range(len(expense_categories)):
        print(f"{i+1}. {expense_categories[i]}")    # add 1 to index for user intuition


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
    """Uploads new expense to expenses.json file. The variable 'expense' should be a dictionary"""
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
    show_categories() 
    expense_category = validate_category_selection()        # validates category selection is within list of categories, returns category selection (int)
    category_selection = select_category(expense_category)  # assigns category selection (int) to category
    merchant = input("Enter Merchant: ")
    note = input("Enter Note: ")
    today = date.today()                            # today's date
    formated_date = today.strftime("%Y-%m-%d")      # formats today's date for json upload (YYYY-mm-dd)

    expense_dict =  {"id":expense_name, 
                     "date":formated_date, 
                     "amount":expense_amount, 
                     "category":category_selection, 
                     "merchant":merchant, 
                     "note":note}
    
    upload_expense(expense_dict)    # uses helper function to add expense_dict dictionary to expenses.json






    



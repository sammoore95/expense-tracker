import json
import uuid
from datetime import date
from decimal import Decimal, InvalidOperation
from tabulate import tabulate
import pandas as pd

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


def validate_monthly_budget_selection():
    """Validate user input is a number in the monthly budget list, returns monthly budget selection (int)"""
    expense_settings = load_settings()
    monthly_budgets = expense_settings["monthly_budgets"]
    num_of_budgets = len(monthly_budgets)
    
    while True:
        user_input = check_for_int("What monthly budget would you like to delete? ")
        if user_input <= num_of_budgets:
            return user_input
        else:
            print("Please enter a valid monthly budget selection")


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
    print(f'Expense for {expense_name} added!')


def show_budget():
    """Prints Monthly budgets"""
    expense_settings = load_settings()
    monthly_budget = expense_settings["monthly_budgets"]
    print("Monthly Budgets:")
    for key, value in monthly_budget.items():
        print(key,":",value)


def add_budget():
    """Adds new monthly budget category and value to settings.json"""
    expense_settings = load_settings()      # loads all expense settings
    monthly_budget = expense_settings["monthly_budgets"]    # selects the monthly budgets dictionary in expense settings

    budget_category = input("What budget category would you like to add? ")
    category_value = float(check_for_decimal("What is your monthly budget for this category? "))

    monthly_budget[budget_category] = category_value    # adds new monthly budget category and value to current dictionary of monthly budgets

    expense_settings["monthly_budgets"] = monthly_budget    # appends new dictionary of monthly budgets to expense settings

    # updates settings.json with updated expense settings
    with open("settings.json", "w") as f:
        json.dump(expense_settings, f, indent=4)

    
def edit_budget():
    """Allows user to update monthly budget category value"""
    expense_settings = load_settings()      #loads settings.json
    monthly_budget = expense_settings["monthly_budgets"]    # selects the monthly budgets dictionary in expense settings

    # validates the user is selecting a current budget category
    while True:
        show_budget()
        budget_selection = input("What budget category would you like to edit? ")
        if budget_selection in monthly_budget.keys():
            break
        else:
            print("Please enter a valid existing category")

    # validates the user is inputing a float to update the selected category to
    new_budget = float(check_for_decimal(f"What is the new budget for {budget_selection}?: "))

    monthly_budget[budget_selection] = new_budget   # updates the selected budget category to the new value

    expense_settings["monthly_budgets"] = monthly_budget    # sets the monthly budgets dictionary in expense settings to the updated monthly values dictionary

    # updates settings.json with updated expense settings
    with open("settings.json", "w") as f:
        json.dump(expense_settings, f, indent=4)


def delete_from_settings():
    """Allows user to delete a category or monthly budget from settings.json"""
    
    # validate user selection
    while True:
        print("""From what settings feature would you like to delete?
          1. Categories
          2. Monthly Budgets""")
        user_selection = check_for_int("Enter selection (int): ")
        if user_selection < 3:
            break
        else:
            print("Please enter a valid selection")

    # delete category
    if user_selection == 1:
        show_categories()
        
        # validate user selected category (index + 1)
        selected_category = validate_category_selection()   

        expense_settings = load_settings()      # load expense settings
        expense_categories = expense_settings["categories"] # select categories
        expense_categories.pop(selected_category-1)     # removes user selected category using the correct index (user selection - 1)
        
        expense_settings["categories"] = expense_categories     # set expense category for expense settings to updated category
        
        # rewrites settings.json with updated expense settings
        with open("settings.json", "w") as f:   
            json.dump(expense_settings, f, indent=4)
        
        print("Category removed from settings!")

    # delete monthly budget
    if user_selection == 2:
        expense_settings = load_settings()  # load expense settings
        expense_budgets = expense_settings["monthly_budgets"]   # select monthly budgets
        
        # print numbered list of monthly budgets
        for i, key in enumerate(expense_budgets):
            print(i+1,". ", key)
        
        # validate user selected budget (index + 1)
        selected_budget = validate_monthly_budget_selection() 
        
        # convert dict keys to a list so we can access by index
        expense_budgets_keys = list(expense_budgets.keys())

        selected_key = expense_budgets_keys[selected_budget - 1]    # map user selection back to key
        expense_budgets.pop(selected_key)   # remove budget based on converted index

        expense_settings["monthly_budgets"] = expense_budgets   # update expense settings with new monthly budget dict

        # rewrites settings.json with updated expense settings
        with open("settings.json", "w") as f:
            json.dump(expense_settings, f, indent=4)

          
def show_budget_table():
    """Create expenses and budget dataframes to perform calculations, then prints table with calculation results"""
    
    # load expenses.json
    with open("expenses.json", "r") as f:
        expenses = json.load(f)

    # load settings.json
    with open("settings.json", "r") as f:
        settings = json.load(f)    

    # budgets dict
    budgets = settings["monthly_budgets"]

    # expenses dataframe
    df_expenses = pd.DataFrame(expenses)
    
    # rename dataframe column from amount to spent, must be done before converting to list below
    df_expenses = df_expenses.rename(columns={"amount":"spent"})    

    # budget dataframe
    df_budgets = pd.DataFrame(budgets.items(), columns=["category", "budget"])

    # group df_expenses dataframe by the category, then sum the amount values in the grouped categories
    spent = df_expenses.groupby("category")["spent"].sum()

    """Merges the df_budgets and spent dataframes.
       In SQL Terms:  FROM df_budgets LEFT OUTER JOIN spent ON df_budgets.category = spent.category"""
    df_summary = df_budgets.merge(spent, on="category", how="left")
    
    # calculations
    df_summary["remaining"] = df_summary["budget"] - df_summary["spent"]    
    df_summary["percent_used"] = ((df_summary["spent"] / df_summary["budget"]) * 100).round(2)

    # copies df_summary to a new dataframe that will be used for formatting and display, ensure df_summary remains safe
    df_summary_fmt = df_summary.copy()

    # format money columns
    money_cols = ["budget", "spent", "remaining"]
    df_summary_fmt[money_cols] = df_summary_fmt[money_cols].applymap(lambda x: f"${x:,.2f}")

    # format percentage columns
    df_summary_fmt["percent_used"] = df_summary_fmt["percent_used"].astype(float).map(lambda x: f"{x:.2f}%")

    # print copy of dataframe summary that is formatted correctly.
    print(tabulate(df_summary_fmt, headers="keys", tablefmt="grid", showindex=False))


def show_category_summary_table():
    """Allows user to select a category,
       then prints a table of all the expenses for the category,
       and prints another table of the summary of expenses for the category"""
    show_categories()
    category_selection = select_category(validate_category_selection())     # returns the name of selected category

    # open expenses.json file
    with open("expenses.json", "r") as f:
        expenses = json.load(f)

    # initialize expenses dict
    category_expenses = []
    
    # adds expense dicts with the selected category to the category_expenses list
    for i in expenses:
        if i["category"] == category_selection:
            category_expenses.append(i)

    # creates expenses dataframe
    df_category_expenses = pd.DataFrame(category_expenses)

    # change datafram column name from "amount" to "spent"
    df_category_expenses = df_category_expenses.rename(columns={"amount":"spent"})

    # copy the original dataframe to a new dataframe for formatting and printing
    df_category_expenses_fmt = df_category_expenses.copy()
    
    # format "spent" column into money formatting
    df_category_expenses_fmt["spent"] = df_category_expenses_fmt["spent"].astype(float).map(lambda x: f"${x:,.2f}")

    # print tabulated expense dataframe
    print("======== Category Expenses ========")
    print(tabulate(df_category_expenses_fmt, headers="keys", tablefmt="grid", showindex=False))

    # copies data to new dataframe from the original category_expesnes dataframe
    df_category_expenses_summary = df_category_expenses.copy()

    # reformates the df_category_expenses_summary to only have 1 row of the selected category
    df_category_expenses_summary = pd.DataFrame(df_category_expenses_summary["category"].unique(), columns=["category"])

    # creates aggregation table to hold the sum and average aggregation from the original df_category_expenses dataframe, aggregated on category
    df_category_expenses_agg = df_category_expenses.groupby("category")["spent"].agg(total_spent="sum", avg="mean")

    # format "total_spent" column into money formatting
    df_category_expenses_agg["total_spent"] = df_category_expenses_agg["total_spent"].astype(float).map(lambda x: f"${x:,.2f}")

    # merges the df_category_expenses_agg dataframe on the df_category_expenses_summary by the category
    df_category_expenses_summary = df_category_expenses_summary.merge(df_category_expenses_agg, on="category", how="left")

    # creates a new dataframe called df_max_spent and creates a max_spent column to be merged into the df_category_expenses_agg dataframe
    df_max_spent = df_category_expenses.loc[[df_category_expenses["spent"].idxmax()]]   # finds the id of the max value in the spent column of df_category_expenses, and returns a new dataframe of the whole row
    df_max_spent["spent"] = df_max_spent["spent"].astype(float).map(lambda x: f"${x:,.2f}") # formats the spent column into money formatting
    df_max_spent["max_spent"] = df_max_spent["id"] + ": " + df_max_spent["spent"].astype(str)   # creates a new row called max_spent in the df_max_spent dataframe that combines the id and the max spent value

    # merges the max_spent column from df_max_spent dataframe to the df_category_expenses_summary dataframe using category
    df_category_expenses_summary = df_category_expenses_summary.merge(df_max_spent[["category", "max_spent"]], on="category", how="left")

    # creates a new dataframe called df_min_spent and creates a min_spent column to be merged into the df_category_expenses_agg datafram
    df_min_spent = df_category_expenses.loc[[df_category_expenses["spent"].idxmin()]]   # finds the id of the min value in the spent column of df_category_expenses, and returns a new dataframe of the whole row
    df_min_spent["spent"] = df_min_spent["spent"].astype(float).map(lambda x: f"${x:,.2f}") # formats the spent column into money formatting
    df_min_spent["min_spent"] = df_min_spent["id"] + ": " + df_min_spent["spent"].astype(str)   # creates a new row called min_spent in the df_min_spent dataframe that combines the id and the max spent value
    
    # merges the min_spent column from df_min_spent dataframe to the df_category_expenses_summary dataframe using category
    df_category_expenses_summary = df_category_expenses_summary.merge(df_min_spent[["category", "min_spent"]], on="category", how="left")

    # print tabulated category summary
    print("======== Category Summary ========")
    print(tabulate(df_category_expenses_summary, headers="keys", tablefmt="grid", showindex=False))


def show_expenses():
    """Show tabulated dataframe of expense.json file"""
    with open("expenses.json", "r") as f:
        expenses = json.load(f)

    # create dataframe of expenses.json
    df_expenses = pd.DataFrame(expenses)

    # format amount column to money formatting
    df_expenses["amount"] = df_expenses["amount"].apply(lambda x: f"${x:,.2f}")

    # print tabulated expenses
    print("===== Expenses ======")
    print(tabulate(df_expenses, headers="keys", tablefmt="grid"))
    

def expense_tracker():
    """Allows for expense budget option selection"""
    while True:
        while True:
            print("""===== Expense Tracker ======
                1. Add Expense
                2. List Expenses
                3. Reports and Analytics
                4. Categories and Budgets
                5. Exit""")
            user_selection = check_for_int("What option would you like to select? (int): ")
            if user_selection <= 5:
                break
            else:
                print("Please select a valid integer from the list")

        if user_selection == 1:
            num_of_expenses = check_for_int("How many expenses would you like to add? (int): ")
            for i in range(num_of_expenses):
                add_expense()
            expense_tracker()
        
        if user_selection == 2:
            show_expenses()
            expense_tracker()

        if user_selection == 3:
            print("""===== Reports =====
                1. Show Monthly Budget Summary
                2. Show Category Budget Summary""")
            while True:
                report_selection = check_for_int("What option would you like to select? (int): ")
                if report_selection <= 2:
                    break
                else:
                    print("Please enter a valid option from the list")

            if report_selection == 1:
                show_budget_table()
            elif report_selection == 2:
                show_category_summary_table()
            expense_tracker()

        if user_selection == 4:
            print("""===== Budget Settings =====
                1. Add Budget
                2. Edit Budget
                3. Delete From Settings""")
            while True:
                settings_selection = check_for_int("What option would you like to select? (int):")
                if settings_selection <= 3:
                    break
                else:
                    print("Please enter a valid option from the list")

            if settings_selection == 1:
                add_budget()
                print("Budget Added!")
                expense_tracker()
            
            if settings_selection == 2:
                edit_budget()
                print("Budget edited!")
                expense_tracker()

            if settings_selection == 3:
                delete_from_settings()
                print("Settings Deleted!")

        if user_selection == 5:
            print("Exiting Budget")
            break
            


expense_tracker()


        


        


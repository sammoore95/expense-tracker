import json

def load_settings():
    with open("settings.json", "r") as f:
        expense_settings = json.load(f)
        return(expense_settings)
    


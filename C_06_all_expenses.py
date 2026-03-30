import pandas
from tabulate import tabulate

# Functions
def num_check(question, num_type="float", exit_code=None):
    """Checks the user enters an integer above 0"""

    if num_type == "int":
        error = "Error. Please enter an integer above 0."
        change_to = int
    else:
        error = "Error. Please enter a number above 0."
        change_to = float

    while True:
        response = input(question)

        if response == exit_code:
            return response

        try:
            response = change_to(response)
            if response > 0:
                return response
            else:
                print(error)

        except ValueError:
            print(error)

def not_blank(question):
    """Checks users don't respond with nothing"""

    while True:
        response = input(question)

        if response != "":
            return response

        print("Sorry, this can't be blank. Please try again.\n")

def get_expenses(exp_type, how_many=1):
    """Gets variable / fixed expenses and outputs
    panda (as a string) and a subtotal of the expenses"""

    # lists for panda
    all_items = []
    all_amounts = []
    all_dollar_per_item = []

    # Expenses dictionary
    expenses_dict = {
        "Item" : all_items,
        "Amount" : all_amounts,
        "$ / Item" : all_dollar_per_item
    }

    amount = how_many
    how_much_question = "How much? $"

    # loop to get expenses
    while True:
        item_name = not_blank("Item Name: ")

        # check users enter at least one variable expense
        if (exp_type == "variable" and item_name == "xxx") and len(all_items) == 0:
            print("Oops - you have not entered anything. "
                  "You need at least one item")
            continue

        elif item_name == "xxx":
            break

        # Get item amount <enter> defaults to number of products made

        # Get variable expenses item amount <enter> defaults to number of
        # products being made
        if exp_type == "variable":

            amount = num_check(f"how many? <enter for {how_many}>: ", "int", "")
            # Allow user to push <enter> to default to number of items being made
            if amount == "":
                amount = how_many

            how_much_question = "Price for one? $"

        # Get price for item (question customized depending on expense type).
        price_for_one = num_check(how_much_question, "float")

        all_items.append(item_name)
        all_amounts.append(amount)
        all_dollar_per_item.append(price_for_one)
        print()

    # make panda
    expense_frame = pandas.DataFrame(expenses_dict)

    # Calculate Row Cost
    expense_frame['Cost'] = expense_frame['Amount'] * expense_frame['$ / Item']

    subtotal = expense_frame['Cost'].sum()

    # Apply currency formatting to all currency columns
    add_dollars = ['$ / Item', 'Cost']
    for var_item in add_dollars:
        expense_frame[var_item] = expense_frame[var_item].apply(currency)

    # Turn amount into string for consistency on table to be left aligned
    expense_frame['Amount'] = expense_frame['Amount'].apply(str)

    # make expense fram into a string with the desired columns
    if exp_type == "variable":
        expense_string = tabulate(expense_frame, headers='keys', tablefmt='psql', showindex=False, colalign=("l", "r", "r", "r"))

    else:
        expense_string = tabulate(expense_frame[['Item', 'Cost']], headers='keys', tablefmt='psql', showindex=False, colalign=("l", "r", "r", "r"))

    # return all items for now so we can check loop
    return expense_string, subtotal

def currency(x):
    """Formats numbers as currency ($#.##)"""
    return "${:.2f}".format(x)


# Main routine

quantity_made = num_check("Quantity being made: ", "int")

print()

print("Getting Variable Costs...")
variable_expenses = get_expenses("variable", quantity_made)
print()
variable_panda = variable_expenses[0]
variable_subtotal = variable_expenses[1]

print("Getting Fixed Costs...")
fixed_expenses = get_expenses("variable", quantity_made)
print()
fixed_panda = fixed_expenses[0]
fixed_subtotal = fixed_expenses[1]


# output area
print("=== Variable Expenses ===")
print(variable_panda)
print(f"Variable Subtotal: ${variable_subtotal:.2f}")

print()

print("=== Fixed Expenses ===")
print(fixed_panda)
print(f"Fixed Subtotal: ${fixed_subtotal:.2f}")

print()
total_expenses = variable_subtotal + fixed_subtotal
print(f"Total Expenses: ${total_expenses:.2f}")

import pandas
from dateutil.utils import today
from tabulate import tabulate
from datetime import date


# Functions

def make_statement(statement, decoration):
    """Emphasises headings by adding decoration
    at the start and end"""

    return f"{decoration * 3} {statement} {decoration * 3}"


def string_check(question, valid_ans_list=('yes', 'no'), num_letters=1):
    """Checks that the users enter the full word
    or the 'n' letter(s) of a word from a list of valid responses"""

    while True:

        response = input(question).lower()

        for item in valid_ans_list:

            # check the response is the entire word
            if response == item:
                return item

            # check the response is the first letter
            if response == item[:num_letters]:
                return item

        print(f"Please choose a valid answer from {valid_ans_list}")


def instructions():
    make_statement("Instructions", "ℹ️")

    print('''
This program will ask you for...
    - The name of the product you are selling
    - How many items you plan on selling
    - The costs for each component of the product
      (variable expenses)
    - Whether or not you have fixed expenses (If you have
      fixed expenses, it will ask you what they are).
    - How much money you want to make (ie: your profit goal)

It will also ask you how much the recommended sales piece should
be rounded to.

The program outputs an itemised list of the variable and fixed
expenses (which includes the subtotals for these expenses).

Finally it will tell you how much you should sell each item for
to reach your profit goal.

The data will also be written to a text file which has the
item name as your product and today's date.

    ''')


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

# assume we have no fixed expenses right now
fixed_subtotal = 0
fixed_panda_string = ""

print(make_statement("Fund Raising Calculator", "💰"))

print()
want_instructions = string_check("Do you want to see the instructions? ")
print()

if want_instructions == "yes":
    instructions()

# Get product details
product_name = not_blank("Product Name: ")
quantity_made = num_check("Quantity being made: ", "int")


print("Let's get Variable Expenses...")
variable_expenses = get_expenses("variable", quantity_made)

variable_panda_string = variable_expenses[0]
variable_subtotal = variable_expenses[1]

# ask user if they have fixed expenses and retrieve them
print()
has_fixed = string_check("Do you have fixed expenses? ")

if has_fixed == "yes":
    fixed_expenses = get_expenses("variable", quantity_made)

    fixed_panda_string = fixed_expenses[0]
    fixed_subtotal = fixed_expenses[1]

    # If the user has not entered any fixed expenses,
    # Set empty panda to "" so that it does not display
    if fixed_subtotal == 0:
        has_fixed = "no"
        fixed_panda_string = ""

total_expenses = variable_subtotal + fixed_subtotal
total_expenses_string = make_statement(f"Total Expenses: ${total_expenses:.2f}", "=")


# Get profit goal here

# strings / output area

# **** Get current date for heading and filename ****
today = date.today()

# Get day, month and year as individual strings
day = today.strftime("%d")
month = today.strftime("%m")
year = today.strftime("%Y")

# Headings / Strings...
main_heading_string = make_statement(f"Fund Raising Calculator "
                                     f"({product_name}, {day}/{month}/{year})", "=")
quantity_string = f"Quantity being made: {quantity_made}"
variable_heading_string = make_statement("Variable Expenses", "-")
variable_subtotal_string = f"Variable Expenses Subtotal: ${variable_subtotal:.2f}"

# Set up strings if we have fixed costs
if has_fixed == "yes":
    fixed_heading_string = make_statement("Fixed Expenses", "-")
    fixed_subtotal_string = f"Fixed Expenses Subtotal: ${fixed_subtotal:.2f}"

# set fixed cost strings to be blank if we don't have fixed costs
else:
    fixed_heading_string = make_statement("You have no Fixed Expenses", "-")
    fixed_subtotal_string = "Fixed Expenses Subtotal: $0.00"

# List of strings to be outputted / written to file
to_write = [main_heading_string, quantity_string,
            "\n", variable_heading_string, variable_panda_string,
            variable_subtotal_string,
            "\n", fixed_heading_string, fixed_panda_string,
            fixed_subtotal_string, "\n",total_expenses_string]


# print area
print()
for item in to_write:
    print(item)

# create file to hold data
file_name = f"{product_name}_{year}_{month}_{day}"
write_to = "{}.txt".format(file_name)

text_file = open(write_to, "w+")

# write the item to file
for item in to_write:
    text_file.write(item)
    text_file.write("\n")

# Functions go here
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

def make_statement(statement, decoration):
    """Emphasises headings by adding decoration
    at the start and end"""

    print(f"{decoration*3} {statement} {decoration*3}")

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

# Main routine goes here

make_statement("Fund Raising Calculator", "💰")

print()
want_instructions = string_check("Do you want to see the instructions? ")

if want_instructions == "yes":
    instructions()

print()
print("program continues...")

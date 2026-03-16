# functions go here
def make_statement(statement, decoration):
    """Emphasises headings by adding decoration
    at the start and end"""

    print(f"{decoration*3} {statement} {decoration*3}")

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


# main routine goes here
make_statement("Fund Raising Calculator", "💰")
print()

instructions = string_check("Do you want to see the instructions? ")

if instructions == "yes":
    print("\nProgram continues...")
elif instructions == "no":
    print("\nProgram continues...")

""" TESTING ENVIROMENT for "Loan Qualifier Application".

This is a command line application to match applicants with qualifying loans.

Example:
    $ python test_qualifier.py
"""
# Import sys module
import sys
# Import Python Fire 
import fire 
# Import Questionary
import questionary

# Import pathlib
from pathlib import Path

# Import fileio
from qualifier.utils.fileio import load_csv, write_csv

# Import Calculators
from qualifier.utils import calculators

# Import Filters
from qualifier.filters.max_loan_size import filter_max_loan_size
from qualifier.filters.credit_score import filter_credit_score
from qualifier.filters.debt_to_income import filter_debt_to_income
from qualifier.filters.loan_to_value import filter_loan_to_value
from qualifier.filters import credit_score
from qualifier.filters import debt_to_income
from qualifier.filters import loan_to_value
from qualifier.filters import max_loan_size

def test_save_csv(qualifying_loans):
    """Saves the qualifying loans to a CSV file.

    Args:
        qualifying_loans (list of lists): The qualifying bank loans.
    """
    # Setting file path to a variable.
    csvpath = Path('./data/output/qualifying_loans.csv')
    write_csv(csvpath, qualifying_loans)	


def test_calculate_monthly_debt_ratio():
    assert calculators.calculate_monthly_debt_ratio(1500, 4000) == 0.375

def test_calculate_loan_to_value_ratio():
    assert calculators.calculate_loan_to_value_ratio(210000, 250000) == 0.84
# Gathering bank data and applicant's information.
def test_filters():
    bank_data = load_csv(Path('./data/daily_rate_sheet.csv'))
    credit_score = 750
    debt = 1500
    income = 4000
    loan = 210000
    home_value = 250000

    monthly_debt_ratio = 0.375
    loan_to_value_ratio = 0.84

    return (bank_data,credit_score, debt, income, loan, home_value,monthly_debt_ratio,loan_to_value_ratio)

def find_qualifying_loans(bank_data,credit_score, debt, income, loan, home_value, monthly_debt_ratio, loan_to_value_ratio ):

    # Run qualification filters
    bank_data_filtered = filter_max_loan_size(loan, bank_data)
    bank_data_filtered = filter_credit_score(credit_score, bank_data_filtered)
    bank_data_filtered = filter_debt_to_income(monthly_debt_ratio, bank_data_filtered)
    bank_data_filtered = filter_loan_to_value(loan_to_value_ratio, bank_data_filtered)
    # Printing the number of loans available.
    print(f"Found {len(bank_data_filtered)} qualifying loans")

    return bank_data_filtered	

    # @TODO: Test the new save_csv code!
def run():
    """The main function for running the script."""

    # Get the applicant's information
    bank_data,credit_score, debt, income, loan, home_value, monthly_debt_ratio, loan_to_value_ratio = test_filters()

    # Find qualifying loans
    qualifying_loans = find_qualifying_loans(
        bank_data,credit_score, debt, income, loan, home_value, monthly_debt_ratio, loan_to_value_ratio 
    )

    # Save qualifying loans
    test_save_csv(qualifying_loans)
# Running main function as main for this app.
if __name__ == "__main__":
    fire.Fire(run)
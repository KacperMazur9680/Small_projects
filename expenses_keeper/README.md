## Expenses keeper

This project facilitates tracking and analyzing given expenses. We can add a new expense and generate a report with ease.
This program also saves given expenses, so they don't have to be written each time. 

## Subcommands and examples:
> add:
It allows the adding of a new expense. If the amount of a given expense is equal to or higher then a 1000, it will be marked on the report.

python .\Small_projects\expenses_keeper\expenses_keeper.py add 150 "Gas - 2020"

python .\Small_projects\expenses_keeper\expenses_keeper.py add 1350 "Gas - 2022"

> report:
Display all the expenses in a table.

python .\Small_projects\expenses_keeper\expenses_keeper.py report

> export-python:
Display all the expenses as a list of objects.

python .\Small_projects\expenses_keeper\expenses_keeper.py export-python

> import-csv:
Import a list of expenses from a csv file.

python .\Small_projects\expenses_keeper\expenses_keeper.py import-csv ".\Small_projects\expenses_keeper\expenses.csv"

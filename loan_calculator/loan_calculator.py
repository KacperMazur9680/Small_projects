from math import *
import argparse
import sys

parser = argparse.ArgumentParser(description="Loan calculator", exit_on_error=False)

parser.add_argument("--type", type=str, help="You HAVE to choose between 'annuity' and 'diff' (differentiated).", )
parser.add_argument("--principal", type=int, help="""The loan's principal ammount.
                                                  You can get it's value if you know the 
                                                  interest, annuity payment, and number of months.""")
parser.add_argument("--periods", type=int, help="""Number of months needed to repay the loan. 
                                                It's calculated based on the interest, annuity payment, and principal.""")
parser.add_argument("--interest", type=float, help="Specified without '%%'. Accepts a floating-point value.")
parser.add_argument("--payment", type=int, help="tos")
args = parser.parse_args()

if not(args.type):
    print("No type specified.")
    sys.exit(1)

args_vals = [args.principal, args.payment, args.periods, args.interest]
existing_args_vals = [arg for arg in args_vals if arg is not None]
conter = 0

for arg in existing_args_vals:
    if arg < 0:
        print("Negative values not accepted.")
        sys.exit(2)

existing_args_vals.append(args.type)
if len(existing_args_vals) < 4:
    print("Not enought argument provided.")
    sys.exit(3)

if args.type == "diff" and args.payment:
    print("Wrong type.")
    sys.exit(4)

#Calculating differentiated payment
if args.type == "diff" and not(args.payment):
    p = args.principal
    i = (args.interest/100/12)
    n = args.periods
    m = 1  # current repayment month
    overpaymnt = 0

    for month in range(n):
        diff_paymnt = ceil((p/n) + i * (p-(p*(m-1)/n)))
        print(f"Month {m}: payment is {diff_paymnt}")
        m += 1
        overpaymnt += diff_paymnt

    print()
    print(f"Overpayment: {overpaymnt-p}")

# Calculating the annuity payment
if args.type == "annuity" and not args.payment:
    p = args.principal
    i = (args.interest / 100) / 12
    n = args.periods

    a_payment = ceil(p * (i * pow(1 + i, n)) / (pow(1 + i, n) - 1))
    overpaymnt = (a_payment * n) - p

    print(f"Your annuity payment = {a_payment}")
    print(f"Overpayment = {overpaymnt}")

# Calculating the loan principal
if args.type =="annuity" and not args.principal:
    a = args.payment
    i = (args.interest / 100) / 12   
    n = args.periods

    loan_prncpl = floor(a / ((i * pow(1 + i, n)) / (pow(1 + i, n) - 1)))
    overpaymnt = (n * a) - loan_prncpl

    print(f"Your loan principal = {loan_prncpl}")
    print(f"Overpayment = {overpaymnt}")

# Calculating how long it will take to repay the loan
if args.type == "annuity" and not args.periods:
    p = args.principal
    i = (args.interest/100)/12
    m = args.payment

    months = ceil(log((m/(m-i*p)), 1+i))
    overpaymnt = (months * m) - p

    if months == 1:
        ans = "It will take 1 month to repay the loan."
    elif 12 > months > 1:
        ans = f"It will take {months} months to repay the loan."
    elif months == 12:
        ans = f"It will take 1 year to repay the loan."
    else:
        years, months = divmod(months, 12)
        if months == 0:
            ans = f"It will take {years} years to repay the loan"
        else:
            ans = f"It will take {years} years and {months} months to repay the loan."

    print(ans)
    print(f"Overpayment = {overpaymnt}")
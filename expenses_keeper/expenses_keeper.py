from csv import DictReader
from dataclasses import dataclass
import pickle
import sys

import click

EXPENSES_FILE = ".\\expenses_keeper\\budget.db"

@dataclass
class Expense:
    id: int
    amnt: int
    desc: str
    big: str = ""
    
    def __post_init__(self):
        if float(self.amnt) <= 0:
            raise ValueError("Nieprawidłowa wartość wydatku.")
        if not self.desc.strip():
            raise ValueError("Brak opisu.")
        if float(self.amnt) >= 1000:
            self.big = "(!)"


def find_free_id(objs: list[Expense]) -> int:
    """Finds the first not used id of a given list of class elements"""
    ids = {o.id for o in objs}
    counter = 1
    while counter in ids:
        counter += 1
    return counter

def stored_expenses() -> list[Expense]:
    """Return a list of arguments if file exists.
    If the file does not exists, return an empty list."""
    try:
        with open(EXPENSES_FILE, "rb") as stream:
            objs = pickle.load(stream)
    except FileNotFoundError:
        objs = []
    return objs

def save_expenses(objs: list[Expense]) -> None:
    """Save the given list to a file, overriding it."""
    with open(EXPENSES_FILE, "wb") as stream:
        pickle.dump(objs, stream)

def add_expense(objs: list[Expense], free_id: int, amount: int, descp: str) -> None:
    """Append to the given list a class argument"""
    obj = Expense(id=free_id, amnt=amount, desc = descp)
    objs.append(obj)

@click.group()
def cli():
    pass

@cli.command()
@click.argument("amount")
@click.argument("descp")
def add(amount: int, descp: str) -> None:
    objs = stored_expenses()
    free_id = find_free_id(objs)

    try:
        add_expense(objs, free_id, amount, descp)
    except ValueError as e:
        print(f"Błąd: {e.args[0]}")
        sys.exit(1)

    save_expenses(objs)
    print("Dodano.")

@cli.command()
def report() -> None:
    objs = stored_expenses()
    if objs:
        print("--ID-- -AMOUNT- -BIG?- --DESCRIPTION------")
        total = 0
        for obj in objs:
            print(f"{obj.id:>6} {obj.amnt:>8} {obj.big:^6} {obj.desc}")
            total += float(obj.amnt)
        print(f"TOTAL: {total:>8}")
    else:
        print("Brak wprowadzonych wydatków.")

@cli.command()
def export_python() -> None:
    objs = stored_expenses()
    if objs:
        export = objs
    else:
        export = "Brak danych do wyświetlenia."
    print(export)

@cli.command()
@click.argument("filename")
def import_csv(filename: str) -> None:
    objs = stored_expenses()
    try:
        with open(filename, "r") as csvfile:
            reader = DictReader(csvfile)
            for row in reader:
                add_expense(objs, free_id=find_free_id(objs), amount=row["amount"], descp=row["description"])
    except FileNotFoundError:
        print("Brak podanego pliku.")
        sys.exit(2)
    
    save_expenses(objs)
    print("Zaimportowano plik.")

if __name__ == "__main__":
    cli()
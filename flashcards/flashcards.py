from io import StringIO
from datetime import datetime
import argparse

class Flashcards:
    def __init__(self) -> None:
        self.base = {}
        self.wrong_ans_base = {}
        self.memory_file = StringIO()

    def add(self) -> None:

        def check_dup(phrase: str) -> None:
            def try_again(card_side: str, phrase: str) -> str:
                flag = True
                while flag:
                    print(f'The {card_side} "{phrase}" already exists. Try again:')
                    self.log_write(self.log_time(), f'The {card_side} "{phrase}" already exists. Try again:')

                    next_phrase = input()
                    if next_phrase not in self.base.keys() and next_phrase not in self.base.values():
                        flag = False
                        return next_phrase

                    phrase = next_phrase

            if phrase in self.base.keys():
                self.term = try_again("term", phrase)
            if phrase in self.base.values():
                self.defin = try_again("definition", phrase)

        while True:
            option = input("\n1. Add a new flashcard\n2. Exit\n")
            self.log_write(self.log_time(), f'1. Add a new flashcard\n2. Exit')
            if option == "1":
                self.log_write(self.log_time(), option)

                self.term = input(f"\nQuestion:\n")
                self.log_write(self.log_time(), f"Question:")
                self.log_write(self.log_time(), self.term)
                check_dup(self.term)

                while True:
                    self.defin = input(f"Answer:\n")
                    self.log_write(self.log_time(), f"Answer:")
                    self.log_write(self.log_time(), self.defin)
                    check_dup(self.defin)
                    if self.defin == "":
                        continue
                    else:
                        break

                self.base.update({self.term:self.defin})
                self.wrong_ans_base.update({self.term:0})

                print(f'The card ("{self.term}":"{self.defin}") has been added.')
                self.log_write(self.log_time(), f'The pair ("{self.term}":"{self.defin}") has been added.')
                continue

            if option == "2":
                self.log_write(self.log_time(), option)
                print()
                break
            
            print(f"{option} is not an option")
            self.log_write(self.log_time(), f"{option} is not an option")

    def remove(self) -> None:
        card = input("Which card?\n")
        self.log_write(self.log_time(), f'Which card?')
        self.log_write(self.log_time(), card)

        if card in self.base.keys():
            self.base.pop(card)
            print("The card has been removed.\n")
            self.log_write(self.log_time(), f'The card has been removed.')

        else:
            print(f'Can\'t remove "{card}": there is no such card.\n')
            self.log_write(self.log_time(), f'Can\'t remove "{card}": there is no such card.')

    def _import(self, outfile=False, outfilename="no_name_added") -> None:
        if not outfile:
            file = input("File name:\n")
            self.log_write(self.log_time(), f'File name:')
            self.log_write(self.log_time(), file)
        else:
            file = outfilename

        try:
            with open("./flashcards/" + file, "r") as stream:
                cards = stream.readlines()

        except FileNotFoundError:
            print("File not found.\n")
            self.log_write(self.log_time(), f'File not found.')

            return None

        num = 0
        for card in cards:
            card = card.replace("\n","")
            card, wrong = card.rsplit(" ", 1)
            card = eval(card)
            self.base.update(card)
            self.wrong_ans_base.update({list(card.keys())[0]: int(wrong)})
            num += 1

        print(f"{num} cards have been loaded.\n")
        self.log_write(self.log_time(), f'{num} cards have been loaded')

    def export(self, outfile=False, outfilename="no_name_added") -> None:
        if not outfile:
            file = input("File name:\n")
            self.log_write(self.log_time(), f'File name:')
            self.log_write(self.log_time(), file)
        else:
            file = outfilename

        num = 0

        with open("./flashcards/" + file, "w") as stream:
            for card in self.base.items():
                term, _ = card
                card = str(card).replace("(","{").replace(")","}").replace(",",":") + f" {self.wrong_ans_base[term]}\n"
                stream.write(card)
                num += 1

        print(f"{num} cards have been saved.\n")
        self.log_write(self.log_time(), f'{num} cards have been saved')

    def ask(self) -> None:
        times = int(input("How many times to ask?\n"))
        self.log_write(self.log_time(), f'How many times to ask?')
        self.log_write(self.log_time(), str(times))
        track = 0

        while track < times:
            for term, defin in self.base.items():
                if track < times:
                    ans = input(f'Print the definition of "{term}":\n')
                    self.log_write(self.log_time(), f'Print the definition of "{term}":')
                    self.log_write(self.log_time(), ans)

                    if ans == defin:
                        print("Correct!")
                        self.log_write(self.log_time(), f"Correct!")
                    else:
                        if ans in self.base.values():
                            for key, val in self.base.items():
                                if val == ans:
                                    print(f'Wrong. The right answer is "{defin}", but your definition is correct for "{key}".')
                                    self.log_write(self.log_time(), f'Wrong. The right answer is "{defin}", but your definition is correct for "{key}".')

                                    self.wrong_ans_base[term] += 1
                        else:
                            print(f'Wrong. The right answer is "{defin}".')
                            self.log_write(self.log_time(), f'Wrong. The right answer is "{defin}".')

                            self.wrong_ans_base[term] += 1

                    track += 1

                else:
                    break

    def log(self) -> None:
        filename = input("File name:\n")
        self.log_write(self.log_time(), "Filename:")
        self.log_write(self.log_time(), filename)

        with open("./flashcards/" + filename, "w") as log:
            for line in self.memory_file:
                log.write(line)

        print("The log has been saved.\n")
        self.log_write(self.log_time(), "The log has been saved.")

    def log_time(self) -> str:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        return current_time

    def log_write(self, time: str, str_log: str) -> None:
        self.memory_file.read()
        self.memory_file.write(f"{time} -> {str_log}\n")
        self.memory_file.seek(0)

    def hardest(self) -> None:
        wrong_ans = dict(sorted(self.wrong_ans_base.items(), reverse=True, key=lambda item: item[1]))
        try:
            most_wrong_val = max(list(wrong_ans.values()))
            if most_wrong_val == 0:
                raise ValueError
            list_of_hardest = ['"'+term+'"' for term in wrong_ans.keys() if wrong_ans[term] == most_wrong_val]
        except ValueError:
            list_of_hardest = []
            print("There are no cards with errors.\n")
            self.log_write(self.log_time(), "There are no cards with errors.")

        if len(list_of_hardest) == 1:
            print(f'The hardest card is {list_of_hardest[0]}. You have {most_wrong_val} errors answering it.\n')
            self.log_write(self.log_time(), f'The hardest card is {list_of_hardest[0]}. You have {most_wrong_val} errors answering it.')

        elif len(list_of_hardest) > 1:
            print(f'The hardest cards are {", ".join(list_of_hardest)}. You have {most_wrong_val} errors answering them.\n')
            self.log_write(self.log_time(), f'The hardest cards are {", ".join(list_of_hardest)}. You have {most_wrong_val} errors answering them')

    def reset_stats(self) -> None:
        for card in self.wrong_ans_base.keys():
            self.wrong_ans_base[card] = 0
        print('Card statistics have been reset.\n')
        self.log_write(self.log_time(), 'Card statistics have been reset.')

    def run(self, action: str) -> None:
        if action == "1":
            self.add()
        if action == "2":
            self.ask()
        if action == "remove":
            self.remove()
        if action == "import":
            self._import()
        if action == "export":
            self.export()
        if action == "log":
            self.log()
        if action == "hardest card":
            self.hardest()
        if action == "reset stats":
            self.reset_stats()

def main():
    fc = Flashcards()
    parser = argparse.ArgumentParser()
    parser.add_argument("--import_from")
    parser.add_argument("--export_to")
    args = parser.parse_args()

    if args.import_from:
        fc._import(outfile=True, outfilename=args.import_from)
        
    while True:
        action = input("1. Add flashcards\n2. Practice flashcards\n3. Exit\n")
        fc.log_write(fc.log_time(), "1. Add flashcards\n2. Practice flashcards\n3.Exit")
        fc.log_write(fc.log_time(), action)

        if action == "3":
            print("\nBye bye!\n")
            if args.export_to:
                fc.export(outfile=True, outfilename=args.export_to)
            break
        else:
            fc.run(action)

if __name__ == "__main__":
    main()

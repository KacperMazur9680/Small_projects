from io import StringIO

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
                    next_phrase = input()
                    if next_phrase not in self.base.keys() and next_phrase not in self.base.values():
                        flag = False
                        return next_phrase

                    phrase = next_phrase

            if phrase in self.base.keys():
                self.term = try_again("term", phrase)
            if phrase in self.base.values():
                self.defin = try_again("definition", phrase)

        self.term = input(f"The card:\n")
        check_dup(self.term)

        self.defin = input(f"The definition of the card:\n")
        check_dup(self.defin)

        self.base.update({self.term:self.defin})
        self.wrong_ans_base.update({self.term:0})

        print(f'The pair ("{self.term}":"{self.defin}") has been added.\n')

    def remove(self) -> None:
        card = input("Which card?\n")
        if card in self.base.keys():
            self.base.pop(card)
            print("The card has been removed.\n")
        else:
            print(f'Can\'t remove "{card}": there is no such card.\n')

    def _import(self) -> None:
        file = input("File name:\n")
        try:
            with open("./flashcards/" + file, "r") as stream:
                cards = stream.readlines()

        except FileNotFoundError:
            print("File not found.\n")
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

    def export(self) -> None:
        file = input("File name:\n")
        num = 0
        
        with open("./flashcards/" + file, "w") as stream:
            for card in self.base.items():
                term, _ = card
                card = str(card).replace("(","{").replace(")","}").replace(",",":") + f" {self.wrong_ans_base[term]}\n"
                stream.write(card)
                num += 1
        
        print(f"{num} cards have been saved.\n")

    def ask(self) -> None:
        times = int(input("How many times to ask?\n"))
        track = 0

        while track < times:
            for term, defin in self.base.items():
                if track < times:
                    ans = input(f'Print the definition of "{term}":\n')
                    if ans == defin:
                        print("Correct!")
                    else:
                        if ans in self.base.values():
                            for key, val in self.base.items():
                                if val == ans:
                                    print(f'Wrong. The right answer is "{defin}", but your definition is correct for "{key}".')
                                    self.wrong_ans_base[term] += 1
                        else:
                            print(f'Wrong. The right answer is "{defin}".')
                            self.wrong_ans_base[term] += 1

                    track += 1

                else:
                    break

    def log(self) -> None:
        filename = input("File name:\n")
        

        """ ask the user where to save the log with the message 'File name:',
        save all the lines that have been input in/output to the console to the file,
        and print the message 'The log has been saved'. Don't clear the log after saving it to the file."""
        """
        from datetime import datetime

        now = datetime.now()

        current_time = now.strftime("%H:%M:%S")
        print("Current Time =", current_time)"""
        pass
    
    def hardest(self) -> None:
        wrong_ans = dict(sorted(self.wrong_ans_base.items(), reverse=True, key=lambda item: item[1]))
        most_wrong_val = max(list(wrong_ans.values()))

        list_of_hardest = ['"'+term+'"' for term in wrong_ans.keys() if wrong_ans[term] == most_wrong_val]

        if len(list_of_hardest) == 1:
            print(f'The hardest card is {list_of_hardest[0]}. You have {most_wrong_val} errors answering it.\n')
        elif len(list_of_hardest) > 1:
            print(f'The hardest cards are {", ".join(list_of_hardest)}. You have {most_wrong_val} errors answering them.\n')
        else:
            print("There are no cards with errors.\n")
    
    def reset_stats(self) -> None:
        for card in self.wrong_ans_base.keys():
            self.wrong_ans_base[card] = 0
        print('Card statistics have been reset.\n')

    def run(self, action: str) -> None:   
        action = action.lower()
        if action == "add":    
            self.add()
        if action == "remove":
            self.remove()
        if action == "import":
            self._import()
        if action == "export":
            self.export()
        if action == "ask":
            self.ask()
        if action == "log":
            self.log()
        if action == "hardest card":
            self.hardest()
        if action == "reset stats":
            self.reset_stats()

def main():
    fc = Flashcards()
    while True:
        action = input("Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):\n")

        if action.lower() == "exit":
            print("Bye bye!")
            break
        else:
            fc.run(action)

if __name__ == "__main__":
    main()

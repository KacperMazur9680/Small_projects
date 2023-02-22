class Flashcards:
    def __init__(self) -> None:
        self.base = {}

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
            self.base.update(eval(card))
            num += 1

        print(f"{num} cards have been loaded.\n")

    def export(self) -> None:
        file = input("File name:\n")
        num = 0
        
        with open(file, "w") as stream:
            for card in self.base.items():
                card = str(card).replace("(","{").replace(")","}").replace(",",":") + "\n"
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
                        else:
                            print(f'Wrong. The right answer is "{defin}".')
                    track += 1

                else:
                    break

    def log(self) -> None:
        """ ask the user where to save the log with the message 'File name:',
        save all the lines that have been input in/output to the console to the file,
        and print the message 'The log has been saved'. Don't clear the log after saving it to the file."""
        pass
    
    def hardest(self) -> None:
        """print a string that contains the term of the card with the highest number of wrong answers, 
        for example, 'The hardest card is "term". You have N errors answering it.' 
        If there are several cards with the highest number of wrong answers, 
        print all of the terms: 'The hardest cards are "term_1", "term_2"'. 
        If there are no cards with errors in the user's answers, print the message 'There are no cards with errors.'"""
        pass
    
    def reset_stats(self) -> None:
        """set the count of mistakes to 0 for all the cards and output the message 'Card statistics have been reset.'"""
        pass

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

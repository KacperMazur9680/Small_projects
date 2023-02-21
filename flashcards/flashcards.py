class Flashcards:
    def __init__(self, num: int) -> None:
        self.base = {}
        self.num = num

    def compare(self) -> None:
        for term, defin in self.base.items():
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
    
    def check_dup(self, phrase: str) -> None:

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

    def run(self):       
        for i in range(self.num):
            self.term = input(f"The term for card #{i+1}:\n")
            self.check_dup(self.term)

            self.defin = input(f"The definition for card #{i+1}:\n")
            self.check_dup(self.defin)

            self.base.update({self.term:self.defin})
        
        self.compare()

def main():
    num = int(input("Input the number of cards:\n"))
    fc = Flashcards(num)
    fc.run()

if __name__ == "__main__":
    main()

class Flashcards:
    def __init__(self, num: int) -> None:
        self.base = {}
        self.num = num
        
        for i in range(self.num):
            term = input(f"The term for card #{i+1}:\n")
            defin = input(f"The definition for card #{i+1}:\n")
            self.base.update({term:defin})

    def compare(self) -> None:
        for term, defin in self.base.items():
            ans = input(f'Print the definition of "{term}":\n')
            if ans == defin:
                print("Correct!")
            else:
                print(f'Wrong. The right answer is "{defin}"')

def main():
    num = int(input("Input the number of cards:\n"))
    fc = Flashcards(num)
    fc.compare()

if __name__ == "__main__":
    main()
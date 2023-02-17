


class Flashcard:
    def __init__(self, term: str, defin: str) -> None:
        self.term = term
        self.defin = defin
    
    def front(self) -> None:
        print("Card:")
        print(self.term)
    
    def back(self) -> None:
        print("Definition:")
        print(self.defin)

    def compare(self, ans: str) -> None:
        if self.defin == ans:
            print("Correct")
        else:
            print("Wrong")

def main():
    term = input() 
    defin = input()
    ans = input()
    fc = Flashcard(term, defin)
    fc.compare(ans) 

if __name__ == "__main__":
    main()
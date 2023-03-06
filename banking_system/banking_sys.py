from random import randint
from sys import exit

class Bank:
    def __init__(self) -> None:
        self.card_database = {}
        self.balance_database = {}

    def create_card(self) -> None:
        def luhn_alg(numbers: str) -> str: 
            list_nums = [num for num in numbers]
            
            multi_odd_id = []
            for id, num in enumerate(list_nums):
                if id % 2 == 0:
                    multi_odd_id.append(int(num)*2)
                else:
                    multi_odd_id.append(int(num))

            list_nums = [num-9 if num > 9 else num for num in multi_odd_id]

            sum_nums = sum(list_nums)
            checksum = 0
            if sum_nums % 10 == 0:
                return str(checksum)
            else:
                while True:
                    if (sum_nums+checksum) % 10 == 0:
                        return str(checksum)
                    else:
                        checksum += 1
                
        bin = "400000"
        while True:
            ident_vars = [str(randint(0,9)) for _ in range(9)]
            acc_ident = "".join(ident_vars)
            if acc_ident not in self.card_database:
                card_num = bin + acc_ident
                checksum = luhn_alg(card_num)
                card_num += checksum
                break
            else:
                continue
        
        card_pin = "".join([str(randint(0,9)) for _ in range(4)])

        self.card_database.update({card_num: card_pin})
        self.balance_database.update({card_num: 0})
        print("\nYour card has been created")
        print(f"Your card number:\n{card_num}")
        print(f"Your card PIN:\n{card_pin}\n")

    def login(self) -> None:
        card_num = input("\nEnter your card number:\n")
        card_pin = input("Enter your PIN:\n")
        if card_num in self.card_database.keys() and self.card_database[card_num] == card_pin:
            print("\nYou have successfully logged in!\n")

            while True:
                sec_options = input("1. Balance\n2. Log out\n0. Exit\n")
                if sec_options == "1":
                    balance = self.balance_database[card_num]
                    print(f"\nBalance: {balance}\n")
                if sec_options == "2":
                    print("\nYou have successfully logged out!\n")
                    self.run()
                if sec_options == "0":
                    print("\nBye!\n")
                    exit()
        else:
            print("\nWrong card number or PIN!\n")
            self.run()

    def run(self) -> None:
        while True:
            frst_options = input("1. Create an account\n2. Log into account\n0. Exit\n")
            if frst_options == "1":
                self.create_card()
            if frst_options == "2":
                self.login()
            if frst_options == "0":
                print("\nBye!\n")
                exit()

def main():
    app = Bank()
    app.run()

if __name__ == "__main__":
    main()
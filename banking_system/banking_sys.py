from random import randint
from sys import exit
import sqlite3

# login changes:
# check balance - done
# "Add income" add said ammount to balance - done
# "Do transfer" transfer money to another account, handle basic transaction errors (ACID) - done
# "Close account" delete the account from db - done
 
class Bank:
    def __init__(self) -> None:
        self.conn = sqlite3.connect("./banking_system/Bank_cards_DB.s3db")
        self.cursor = self.conn.cursor()
 
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Bank_cards (
        id INTEGER PRIMARY KEY,
        number VARCHAR(16) UNIQUE,
        pin VARCHAR(4),
        balance INTEGER DEFAULT 0
        );""")

    def luhn_alg(self, numbers: str) -> str: 
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

    def create_card(self) -> None:
        bin = "400000"
        self.cursor.execute("""SELECT number FROM Bank_cards;""")
        num_list = self.cursor.fetchall()
        
        while True:
            ident_vars = [str(randint(0,9)) for _ in range(9)]
            acc_ident = "".join(ident_vars)
            card_num = bin + acc_ident
            checksum = self.luhn_alg(card_num)
            card_num += checksum

            if card_num not in num_list:
                break
            else:
                continue
        
        card_pin = "".join([str(randint(0,9)) for _ in range(4)])

        self.cursor.execute(f"""
        INSERT INTO Bank_cards(number, pin)
        VALUES ({card_num}, "{card_pin}");""")

        # Checking if DB takes data correctly
        # self.cursor.execute("""SELECT * from Bank_cards""")
        # print(self.cursor.fetchall())

        print("\nYour card has been created")
        print(f"Your card number:\n{card_num}")
        print(f"Your card PIN:\n{card_pin}\n")

    def login(self) -> None:
        card_num = input("\nEnter your card number:\n")
        card_pin = input("Enter your PIN:\n")

        try:
            self.cursor.execute(f"""
            SELECT pin FROM Bank_cards
            WHERE number={card_num};""")

            pin = self.cursor.fetchone()[0]

            if card_pin != pin:
                raise TypeError

        except TypeError:
            print("\nWrong card number or PIN!\n")
            self.run()

        print("\nYou have successfully logged in!\n")

        while True:
            sec_options = input("1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit\n")

            self.cursor.execute(f"""
            SELECT balance FROM Bank_cards
            WHERE number={card_num};""")
            balance = self.cursor.fetchone()[0]

            if sec_options == "1":
                print(f"\nBalance: {balance}\n")

            if sec_options == "2":
                income = input("\nEnter income:\n")

                if income.isdigit():
                    new_balance = int(balance) + int(income)
                    new_balance = str(new_balance)

                    self.cursor.execute(f"""
                    UPDATE Bank_cards
                    SET balance = {new_balance}
                    WHERE number = {card_num};""")
                    print("Income was added!\n")
                
                else:
                    print("\nInvalid income, try again.\n")
            
            if sec_options == "3":
                print("\nTransfer\n")
                acc_to_transf = input("Enter card number:\n")

                self.cursor.execute("""
                SELECT number FROM Bank_cards""")
                nums_list = [num[0] for num in self.cursor.fetchall()]


                if acc_to_transf not in nums_list:
                    if self.luhn_alg(acc_to_transf[:-1]) != acc_to_transf[-1]:
                        print("Probably you made a mistake in the card number. Please try again!\n")
                        continue
                    else:
                        print("Such a card does not exist.\n")
                        continue

                if acc_to_transf == card_num:
                    print("You can't transfer money to the same account!\n")
                    continue

                amount = input("Enter how much money you want to transfer:\n")
                if amount.isdigit():
                    if int(balance) - int(amount) < 0:
                        print("Not enough money!\n")
                        continue
                else:
                    print("\nInvalid income, try again.\n")

                self.cursor.execute(f"""
                UPDATE Bank_cards
                SET balance = {int(balance)-int(amount)}
                WHERE number = {card_num}""")

                self.cursor.execute(f"""
                SELECT balance FROM Bank_cards
                WHERE number = {acc_to_transf}""")
                
                acc_to_transf_balance = self.cursor.fetchone()[0]
                
                self.cursor.execute(f"""
                UPDATE Bank_cards
                SET balance = {int(acc_to_transf_balance) + int(amount)}
                WHERE number = {acc_to_transf}""")

                print("Success!\n")

            if sec_options == "4":
                self.cursor.execute(f"""DELETE FROM Bank_cards WHERE number={card_num};""")
                print("\nThe account has been closed!\n")
                
            if sec_options == "5":
                print("\nYou have successfully logged out!\n")
                self.run()

            if sec_options == "0":
                print("\nBye!\n")
                self.conn.commit()
                self.conn.close()
                exit()

    def run(self) -> None:
        while True:
            frst_options = input("1. Create an account\n2. Log into account\n0. Exit\n")
            if frst_options == "1":
                self.create_card()
            if frst_options == "2":
                self.login()
            if frst_options == "0":
                print("\nBye!\n")
                self.conn.commit()
                self.conn.close()
                exit()

def main():
    app = Bank()
    app.run()

if __name__ == "__main__":
    main()
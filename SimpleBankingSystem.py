# Program start menu
import random
from luhn import *
import sqlite3

# Do connect with sql
conn = sqlite3.connect('card.s3db')
cur = conn.cursor()

cur.execute('drop table if exists card')
conn.commit()

# Create table
cur.execute(
    """
    CREATE TABLE IF NOT EXISTS 'card' (
        id INTEGER,
        number TEXT,
        pin TEXT,
        balance INTEGER DEFAULT 0
    )
    """
)
conn.commit()

random.seed(42)

class Card:
    """
    class for credit card
    props: card number, pin, balance
    methods: balance_q - check balance
             log_in
             log_out
             create_card - create card with Luhn check algo
             add_income - add to balance
             check_card - perform checking for next transfer
             close_acc - delete account
             transfer - perform transfer from self.acc to other
    """

    def __init__(self):
        self.card_no = None
        self.pin = None
        self.balance = 0
        self.id = random.randint(1, 1000)

    def balance_q(self):
        cur.execute(
            """
            SELECT balance FROM card
            WHERE number = {}
            """.format(self.card_no)
        )
        data = cur.fetchall()
        print("Balance: {}".format(data[0][0]))

    def log_in(self, card, pin):
        cur.execute(
            """
            SELECT *
            FROM card
            WHERE number = {0} AND pin = {1}
            """.format(card, pin)
        )
        data = cur.fetchall()
        self.card_no = card
        self.pin = pin
        for cpb in data:
            if cpb[1] == card:
                if cpb[2] == pin:
                    self.balance = cpb[3]
                    return True

    def log_out(self):
        self.card_no = None
        self.pin = None

    def create_card(self):
        can = ""
        pin = ""
        iin = "400000"
        for i in range(0, 9):
            can += str(random.randint(1, 9))

        self.card_no = iin + can

        self.card_no = append(self.card_no)

        for i in range(4):
            pin += str(random.randint(0, 9))
        self.pin = pin
        self.id += 1
        print(f"Your card has been created\n"
              f"Your card number:\n{self.card_no}\n"
              f"You card PIN:\n{self.pin}")
        cur.execute("INSERT INTO card VALUES (?, ?, ?, ?)", (None, self.card_no, self.pin, 0))
        conn.commit()

    def add_income(self, amount: int):
        cur.execute(
            """
            SELECT balance
            FROM card
            WHERE number = {}
            """.format(self.card_no)
        )
        db_balance = cur.fetchall()[0][0]
        db_balance += int(amount)

        self.balance = db_balance
        cur.execute("UPDATE card SET balance = {0} WHERE number = {1} ".format(db_balance, self.card_no))
        print("Income was added!")
        conn.commit()

    def check_card(self, value: str):
        if not (verify(value)):
            print("Probably you made a mistake in the card number. Please try again!")
            return False, 0
        if self.card_no == value:
            print("You can't transfer money to the same account!")
            return False, 0
        card_list = cur.execute("SELECT number, balance FROM card").fetchall()
        card_list = [i[0] for i in card_list]
        print(card_list)
        if value not in card_list:
            print("Such a card does not exist.")
            return False, 0
        print("S balance {}".format(self.balance))
        return True, self.balance

    def transfer(self, number, money):
        # Execute SQL update
        cur.execute(
            "UPDATE card SET balance=balance-{0} WHERE number={1}".format(int(money), self.card_no)
        )
        cur.execute(
            "UPDATE card SET balance={0} WHERE number={1}".format(int(money), number)
        )
        conn.commit()
        print("Success!")

    def close_acc(self):
        cur.execute(
            """
            DELETE FROM card
            WHERE number = {}
            """.format(self.card_no)
        )
        conn.commit()
        self.card_no = None
        self.pin = None
        self.id = None
        self.balance = 0

        print("The account has been closed!")
        pass


while True:
    menu = input(
        f"1. Create an account\n"
        f"2. Log into account\n"
        f"0. Exit\n"
    )
    if menu == "1":
        new_card = Card()
        new_card.create_card()
    elif menu == "2":
        card_no = input("Enter your card number:\n")
        card_pin = input("Enter your PIN:\n")
        existing_card = Card()
        status = existing_card.log_in(card_no, card_pin)
        if status:
            print("You have successfully logged in!")
            log_out = False
            while not log_out:
                menu_2 = input(
                    f"1. Balance\n"
                    f"2. Add income\n"
                    f"3. Do transfer\n"
                    f"4. Close account\n"
                    f"5. Log out\n"
                    f"0. Exit\n"
                )
                if menu_2 == "1":
                    existing_card.balance_q()

                elif menu_2 == "2":
                    income = input("Enter income:\n")
                    existing_card.add_income(int(income))
                elif menu_2 == "3":
                    print("Transfer")
                    enter_card = input("Enter card number:\n")
                    chck_status, my_money = existing_card.check_card(enter_card)
                    if chck_status:
                        enter_money = input("Enter how much money you want to transfer:\n")
                        if my_money < int(enter_money):
                            print("Not enough money!")
                            pass
                        else:
                            existing_card.transfer(enter_card, enter_money)

                elif menu_2 == "4":
                    existing_card.close_acc()
                    log_out = True
                elif menu_2 == "5":
                    print("You have successfully logged out!")
                    log_out = True
                elif menu_2 == "0":
                    print("Bye!")
                    quit()

        else:
            print("Wrong card number or PIN!")
            continue

    if menu == '0':
        print("Bye!")
        quit()

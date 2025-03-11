import os
from abc import ABC, abstractmethod

class AccountHolderBase(ABC):

    @abstractmethod
    def get_account_holder_details(self):
        """Abstract method"""

    @abstractmethod
    def withdraw_amount(self, balance):
        """Abstract method"""

    @abstractmethod
    def add_amount(self, balance):
        """Abstract method"""


class AccountHolder(AccountHolderBase):
    
    def __init__(self, account_number, balance, account_holder_name):
        self.account_number = account_number
        self.balance = balance
        self.account_holder_name = account_holder_name


    def get_account_holder_details(self):
        return f"{self.account_number} {self.balance} {self.account_holder_name}"

    
    def withdraw_amount(self, amount):
        if self.balance < amount:
            print("Cannot withdraw due to insufficient balance.")
        else:
            self.balance -= balance

    
    def add_amount(self, amount):
        self.balance += amount


prefix_filename = input("Please enter filename")
new_master_file_path = f"./{prefix_filename}.new.txt"
new_old_master_file_path = f"./{prefix_filename}.old.txt"

if not os.path.exists(new_old_master_file_path):
    with open("sample.master.old.txt", 'r') as sample_file:








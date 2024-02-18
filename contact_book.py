"""
Created on Sat Mar  4 19:59:52 2023

@author: behniya
"""

"""This program is a simple contact book
========================================
========================================
        Aouthor : Behniya Ganji
        Date   :  Saturday , 04 / 03
        Ending data : Sunday , 12 / 03
========================================
========================================            
"""

import os
import re 
import sys
import sqlite3
from sqlite3 import Error

class Contacts_and_informations:
    """This is a contact book class wich store contact informations"""
    def get_name(self) -> str:
        """This method is to get contact name"""
        file_adress = 'contact_book.txt'
        self.contact_name = input("Enter what you want to save this contact:")
        with open(file_adress , 'a') as file:
            file.write("\n\t")
            file.write(self.contact_name.capitalize())
            file.write('\n')
            
        return self.contact_name.capitalize()
    
    def get_phone_numb(self) -> str: 
        """This method is to get contact phone number"""
        file_adress = 'contact_book.txt'
        phone_number_numbs = input("How many numbers do you want to save for this contact? :")
        while True:
            if re.search('[A-Z]' , phone_number_numbs) or re.search('[a-z]' , phone_number_numbs):
                print("inValid value!\n Try again\n")
                phone_number_numbs = input("How many numbers do you want to save for this contact? :")
            else:
                phone_number_numbs = int(phone_number_numbs)
                break
        self.contact_phone_numbers = []
        for i in range(phone_number_numbs):
            inVar = input(f'Enter the contact number {i+1}:')
            self.contact_phone_numbers.append(inVar)
            try:
                if i == 0:
                    with open(file_adress , 'a') as file:
                        file.write('----------------------------------------\n')
                        file.write('----------------------------------------\n')
                        file.write('\n\t')
                        file.write(inVar + ' , ')
                elif i == 1:
                    with open(file_adress , 'a') as file:
                        file.write('\t')
                        file.write(inVar)
            except FileNotFoundError:
                if i == 0:
                    with open(file_adress , 'w') as file:
                        file.write('----------------------------------------\n')
                        file.write('----------------------------------------\n')
                        file.write('\n\t')
                        file.write(inVar + ' , ')
                elif i == 1:
                    with open(file_adress , 'w') as file:
                        file.write('\t')
                        file.write(inVar + ' , ')
        list_len = len(self.contact_phone_numbers)
        temp = ''
        for i in range(list_len):
            temp = temp + str(self.contact_phone_numbers[int(i)]) + ' , '
        return temp
    def get_email_adress(self) -> str:
        """This method is to get contact email adress"""
        file_adress = 'contact_book.txt'
        print("(Email adress is optional type none to leave this field empty)")
        print("Enter email adress with out @gmail.com")
        self.contact_email_adress = input("Enter the contact email adress:")
        if self.contact_email_adress == 'none' or self.contact_email_adress == 'None':
            self.contact_email_adress = " "
        while True:
            if re.search('@gmail.com', self.contact_email_adress):
                print("Invalid value!\n try again!")
            else:
                break
        with open(file_adress , 'a') as file:
            file.write("\n\t")
            file.write(self.contact_email_adress)
        
        return self.contact_email_adress
    
    def contact_informations(self , contact_name: str , contact_phone_numb: str , contact_email_adress: str) ->tuple:
        """This function store contact informations in a list"""
        self.contact = (contact_name , contact_phone_numb , contact_email_adress)
        return self.contact
    
def show_contact_book() -> None:
    """This function is to show the contact book with stored
    informations"""
    file_adress = 'contact_book.txt'
    try:
        with open(file_adress) as file:
           for i in file:
               print(i)
    except FileNotFoundError:
        print("Contact book is empty!")

def show_menue():
    """The menue design"""
    print("\n\n1. Create a new contact")
    print("\n2. Edit a contact")
    print("\n3. Delete a contact")
    print("\n4. Search for a contact")
    print("\n5. Show contact book")
    print("\n6. Exite")
    
    client_choice = int(input("Enter your choise:"))
    if client_choice == 1:
        contact = Contacts_and_informations()
        phone = contact.get_phone_numb()
        email = contact.get_email_adress()
        name = contact.get_name()
        informations = (name , phone , email)
        insert_into_db(informations)
        show_menue()
    elif client_choice == 2:
        editing_contact()
        show_menue()
    elif client_choice == 3:
        deleting_contact()
        show_menue()
    elif client_choice == 4:
        searching_contact()
        show_menue()
    elif client_choice == 5:
        show_contact_book()
        show_menue()
    elif client_choice == 6:
        print("------Good Bye------")
        sys.exit()
    else:
        print("Invalid value!\n Try again!\n\n") 
    
def sql_connection():
    """This function is to make a mini database"""
    try:
        con = sqlite3.connect('contact_database.db')
    except Error:
        pass
    return con

def sql_cursor(con):
    """This function is to make an cursor object that allow us to
    execute database's statements"""
    cur = con.cursor()
    return cur

def create_table():
    """This function is to make a table in our database"""
    con = sql_connection()
    cur = sql_cursor(con)
    cur.execute("CREATE TABLE contacts_data(name,phone,email)")
    con.commit()
    con.close()
    
def insert_into_db(informations : tuple):
    """This function is to insert the informations and store them
    in the contact_database.db database"""
    con = sql_connection()
    cur = sql_cursor(con)
    inVar00 = "INSERT INTO contacts_data(name,phone,email) VALUES(?,?,?);"
    inVar01 = informations
    cur.execute(inVar00 , inVar01)
    con.commit()
    con.close() 

def searching_contact() ->None:
    """This function is to search for a contact
    and show contact informations client is searching for"""
    name = input("Enter the contact name you are searching for:")
    name = name.capitalize()
    con = sql_connection()
    cur = sql_cursor(con)
    cur.execute("SELECT phone,email FROM contacts_data WHERE name=?",(name,))
    records = cur.fetchone()
    if records is None:
        print("No such contact in your contact book was found!")
    else:
        for i in records:
            print(i)
    con.commit()
    con.close()
    
def deleting_contact() -> None:
    """This function is to delete a contact and it's informations"""
    file_adress = 'contact_book.txt'
    inVar01 = input("Enter the name you want to be deleted:")
    inVar01 = inVar01.capitalize()
    con = sql_connection()
    cur = sql_cursor(con)
    inVar00 = "SELECT name,phone,email FROM contacts_data WHERE name = ?"
    cur.execute(inVar00 , (inVar01,))
    records = cur.fetchone()
    inVar02 = "DELETE FROM contacts_data WHERE name = ?"
    if records is None:
        print("No such contact in your contact book was found!")
    else:
        cur = sql_cursor(con)
        cur.execute(inVar02,(inVar01,))
        print(f'{inVar01}  is deleted successfully')
    con.commit()
    con.close()  

def editing_contact():
    """This function is to changes the column values in database
    and change the contact informations in clinet's command order"""
    def editing_name(inVar00):
        """This function is to edit the contact name and store new values
        in the data base and save the changes at the end"""
        con = sql_connection()
        cur = sql_cursor(con)
        inVar02 = input("Enter the name you want to be replaced:")
        inVar02 = inVar02.capitalize()
        inVar01 = "UPDATE contacts_data SET name=? WHERE name=?"
        rp_data = [inVar02 , inVar00]
        cur.execute(inVar01 , rp_data)
        con.commit()
        con.close()
    
    def editing_phone(inVar00):
        """This function is to edit the contact phone and store new values
        in the data base and save the changes at the end"""
        con = sql_connection()
        cur = sql_cursor(con)
        phone_numbers = []
        inVar02 = ''
        phone_number_numbs = int(input("Enter how many numbers do you wanna enter for this contact:"))
        for i in range(phone_number_numbs):
            numbers = input(f'Enter number {i+1}:')
            phone_numbers.append(numbers)
        list_len = len(phone_numbers)
        for i in range(list_len):
            inVar02 = inVar02 + str(phone_numbers[int(i)]) + ' , '
        inVar01 = "UPDATE contacts_data SET phone=? WHERE name=?"
        rp_data = [inVar02 , inVar00]
        cur.execute(inVar01 , rp_data)
        con.commit()
        con.close()
    
    def editing_email(inVar00):
        """This function is to edit the contact email and store new values
        in the data base and save the changes at the end"""
        con = sql_connection()
        cur = sql_cursor(con)
        print("(Email adress is optional type none to leave this field empty)")
        print("Enter email adress with out @gmail.com")
        inVar01 = input("Enter the contact new email adress:")
        if inVar01 == 'None' or inVar01 == 'none':
            inVar01 == " "
        while True:
            if re.search('@gmail.com' , inVar01):
                print("Invalid vale\nTry again!")
                inVar01 = input("Enter the contact new email adress:")
            else:
                break
        rp_data = [inVar01 , inVar00]
        inVar02 = "UPDATE contacts_data SET email=? WHERE name=?"    
        cur.execute(inVar02 , rp_data)    
        con.commit()
        con.close()
        
    inVar00 = input("Enter the name you want to edit:")
    inVar00 = inVar00.capitalize()
    print("\nWhat do you want to edit?\n")
    print("1. Edit contact name")
    print("2. Edit contact phone")
    print("3. Edit contact email")
    print("4. Edit all informations about contact")
    
    client_choice = int(input("Enter your choice:"))
    if client_choice == 1:
        editing_name(inVar00)
    elif client_choice == 2:
        editing_phone(inVar00)
    elif client_choice == 3:
        editing_email(inVar00)
    elif client_choice == 4:
        editing_name(inVar00)
        editing_phone(inVar00)
        editing_email(inVar00)
    else:
        print("\nInvalid value!")
    
    
print("-----------------contact book-----------------")
show_menue()
try:
    con = sql_connection()
    cur = sql_cursor(con)
    cur.execute("CREATE TABLE IF NOt EXISTS contacts_data(name,phone,email)")
    con.commit()
    con.close()
except:
    pass
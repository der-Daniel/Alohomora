#!/usr/bin/python3

# ------------------------------------------------------------------------------

# PIP
import readline

# Alohomora
from app import completer
from app import db
from app import shell_io

# ------------------------------------------------------------------------------


def edit():
    print('Which Account do you want to delete?')
    accounts = db.get_accounts()
    text_completer = completer.TextCompleter(accounts)
    readline.set_completer(text_completer.complete)
    readline.parse_and_bind('tab: complete')
    account = input("Account: ")
    while(account not in accounts):
        print('\'{0}\' is not in your database'.format(account))
        account = input("Account: ")
    id, name, salt, length, lowercase, uppercase, numbers, specials = db.get_account(
        account)
    print('')
    print(name)
    print('Databse id: ' + str(id))
    print('Salt (first 20 digits): ' + salt[0:20] + '..')
    print('Length: ' + str(length))
    print('Character Sets:')
    print('Lowercase: ' + lowercase)
    print('Uppercase: ' + uppercase)
    print('Numbers: ' + numbers)
    print('Specials: ' + specials)
    print('\nWhat do you want do you?')
    g = shell_io.key_input('(G)enerate new Salt, Change (C)haracter Sets, Change Password (L)ength: ', ['g', 'G', 'c', 'C', 'l', 'L'])
    print('')
    if(g == 'g' or g == 'G'):
        db.update_salt(name)
        print("A new salt has successfully been generated.")
    elif(g == 'c' or g == 'C'):
        lowercase = shell_io.get_lowercase(lowercase)
        uppercase = shell_io.get_uppercase(uppercase)
        numbers = shell_io.get_numbers(numbers)
        specials = shell_io.get_specials(specials)
        db.update_character_sets(name, lowercase, uppercase, numbers, specials)
    elif(g == 'l' or g == 'L'):
        length = shell_io.get_length(length)
        db.update_length(name, length)
    print('\nDatabase successfully updated.')

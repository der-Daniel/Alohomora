#!/usr/bin/python3

# ------------------------------------------------------------------------------

# PIP
import readline

# Alohomora
from app import completer
from app import db
from app import shell_io

# ------------------------------------------------------------------------------


def delete():
    print('Which Account do you want to delete?')
    accounts = db.get_accounts()
    text_completer = completer.TextCompleter(accounts)
    readline.set_completer(text_completer.complete)
    readline.parse_and_bind('tab: complete')
    account = input("Account: ")
    while(account not in accounts):
        print('\'{0}\' is not in your database'.format(account))
        account = input("Account: ")
    g = shell_io.key_input("Delete '{0}', are you sure? (y/n)".format(account),
                           ['n', 'N', 'y', 'Y', ''])
    if(g == 'y' or g == 'Y' or g == ''):
        try:
            db.delete_account(account.strip())
            print(
                "\nSuccessfully deleted '{0}' from the database.".format(account))
        except Error:
            print('An error occurred during database processing. :(')

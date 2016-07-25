#!/usr/bin/python3

# ------------------------------------------------------------------------------

# Copyright reference for pyperclip

# pyperclip
# Copyright (c) 2014, Al Sweigart
# All rights reserved.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
# IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
# TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
# PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
# TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS

# ------------------------------------------------------------------------------
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# imports

import sys
from os import path
import re

import db
import pw_gen
import hashlib

import pyperclip
import getpass
import completer
import readline

# ------------------------------------------------------------------------------


db_file = path.join(path.dirname(
    path.realpath(__file__)), 'database/db.sqlite3')


def copy_to_clipboard(pw):
    pyperclip.copy(pw.decode('utf-8'))


def init():
    if(not path.isfile(db_file)):
        print('No database was found.')
        print('If you already have a database, move it to \'database/\'.')
        print('If this is the first time you use Alohomora, you can create\n\
a new database.\n')
        print('What do you want me to do?')
        g = ''
        while(g != 'C' and g != 'c' and g != 'E' and g != 'e'):
            g = input('(C)reate new one, (E)xit: ')
        if(g == 'E' or g == 'e'):
            sys.exit(0)
        else:
            db.init()
            print('Database successfully created.\n\n')


def enter_secret():
    secret = ''
    b = False
    while(not b):
        secret = getpass.getpass("Enter your Secret: ")
        fingerprint = hashlib.sha512(secret.encode('utf-8')).hexdigest()
        print("\nfingerprint:")
        print('-------------------')
        print(fingerprint[0:19] + '\n' + fingerprint[20:39])
        print('-------------------\n')
        g = input("ok? (y/n)")
        while(g != 'n' and g != 'N' and g != 'y' and g != 'Y' and g != ''):
            g = input("ok? (y/n)")
        if(g == 'n' or g == 'N'):
            b = False
            print("\n------------------------------\n")
        if(g == 'y' or g == 'Y' or g == ''):
            b = True
    return secret


def get_lowercase():
    lowercase = input("lowercase (type 'a-z' for default): ").strip()
    while(len(re.findall(r"[a-z]", lowercase)) != len(lowercase) and lowercase != 'a-z'):
        print('Only lowercase letters are allowed.')
        lowercase = input("lowercase (type 'a-z' for default): ").strip()
    if(lowercase == 'a-z'):
        return 'abcdefghijklmnopqrstuvwxyz'
    return lowercase


def get_uppercase():
    uppercase = input("uppercase (type 'A-Z' for default): ").strip()
    while(len(re.findall(r"[A-Z]", uppercase)) != len(uppercase) and uppercase != 'A-Z'):
        print('Only uppercase letters are allowed.')
        uppercase = input("uppercase (type 'A-Z' for default): ").strip()
    if(uppercase == 'A-Z'):
        return 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    return uppercase


def get_numbers():
    numbers = input("numbers (type '0-9' for default): ").strip()
    while(len(re.findall(r"[0-9]", numbers)) != len(numbers) and numbers != '0-9'):
        print('Only numbers are allowed.')
        numbers = input("numbers (type '0-9' for default): ").strip()
    if(numbers == '0-9'):
        return '0123456789'
    return numbers


def get_character_sets():
    print('Character Sets:')
    lowercase = get_lowercase()
    uppercase = get_uppercase()
    numbers = get_numbers()
    specials = input('special characters: ').strip()
    return lowercase, uppercase, numbers, specials


def add_account(name):
    length = 40
    lowercase = 'abcdefghijklmnopqrstuvwxyz'
    uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    numbers = '0123456789'
    specials = '#!?/=+-'
    print('{0} is to be added to the database.'.format(name))
    print('By default the password length is set to 40 and a-z, A-Z, 0-9 and #!?/=+- are used as character sets.')
    print('However some web services have some ridiculous limitations...')
    print('Do you want to change the default configurations?')
    g = ''
    while(g != 'y' and g != 'Y' and g != 'n' and g != 'N'):
        g = input('(Y)es, (No): ')
    if(g == 'y' or g == 'Y'):
        print('\nLength:')
        length = int(input('password length: '))
        print('Character Sets:')
        lowercase, uppercase, numbers, specials = get_character_sets()
    db.add_account(name, length, lowercase, uppercase, numbers, specials)
    print('\n\'{0}\' has successfully been added to the database.\n'.format(name))


def get_password(secret):
    accounts = db.get_accounts()
    text_completer = completer.TextCompleter(accounts)
    readline.set_completer(text_completer.complete)
    readline.parse_and_bind('tab: complete')
    while(True):
        account = input("Account: ")
        if(account not in accounts):
            g = input(
                "'" + account + "' is not in your database base yet, wanna add it? (y/n)")
            while(g != 'n' and g != 'N' and g != 'y' and g != 'Y' and g != ''):
                g = input("wanna add it? (y/n)")
            if(g == 'y' or g == 'Y' or g == ''):
                add_account(account)
                text_completer.update(account)
                accounts.append(account)
                print("~~~ '" + account + "' was added to your database ~~~")
            if(g == 'n' or g == 'N'):
                continue

        _, _, salt, length, lowercase, uppercase, numbers, specials = db.get_account(
            account)
        password = pw_gen.get_password(
            secret, salt, length, lowercase, uppercase, numbers, specials)
        pyperclip.copy(password)
        print()
        print('first 5 letters: ' + password[0:5])
        print('~~~ copied to clipboard ~~~')
        print("\n------------------------------\n")


def edit_password():
    print('Which Account do you want to delete?')
    accounts = db.get_accounts()
    text_completer = completer.TextCompleter(accounts)
    readline.set_completer(text_completer.complete)
    readline.parse_and_bind('tab: complete')
    account = input("Account: ")
    while(account not in accounts):
        print('\'{0}\' is not in your database'.format(account))
        account = input("Account: ")
    id, name, salt, length, lowercase, uppercase, numbers, specials = db.get_account(account)
    print('')
    print(name)
    print('databse id: ' + str(id))
    print('salt (first 20 digits): ' + salt[0:20] + '..')
    print('password length: ' + str(length))
    print('Character Sets:')
    print('lowercase: ' + lowercase)
    print('uppercase: ' + uppercase)
    print('numbers: ' + numbers)
    print('specials: ' + specials)
    print('\nWhat do you want do you?')
    g = input('(G)enerate new Salt, Change (C)haracter Sets, Change Password (L)ength: ')
    while(g != 'g' and g != 'G' and g != 'c' and g != 'C' and g != 'l' and g != 'L'):
        g = input('(G)enerate new Salt, Change (C)haracter Sets, Change Password (L)ength: ')
    if(g == 'g' or g == 'G'):
        db.update_salt(name)
        print("A new salt has successfully been generated.")
    elif(g == 'c' or g == 'C'):
        lowercase, uppercase, numbers, specials = get_character_sets()
        db.update_character_sets(name, lowercase, uppercase, numbers, specials)
    elif(g == 'l' or g == 'L'):
        g = input('New Length: ')
        while(True):
            try:
                l = int(g)
                if(l > 0):
                    break
            except ValueError:
                pass
            g = input('Input is not a positive integer: ')
        db.update_length(name, l)
        print("Length successfully changed to '{0}'.".format(g))


def delete_password():
    print('Which Account do you want to delete?')
    accounts = db.get_accounts()
    text_completer = completer.TextCompleter(accounts)
    readline.set_completer(text_completer.complete)
    readline.parse_and_bind('tab: complete')
    account = input("Account: ")
    while(account not in accounts):
        print('\'{0}\' is not in your database'.format(account))
        account = input("Account: ")
    g = input("Delete '{0}', are you sure? (y/n)".format(account))
    while(g != 'n' and g != 'N' and g != 'y' and g != 'Y' and g != ''):
        g = input("Delete '{0}', are you sure? (y/n)".format(account))
    if(g == 'y' or g == 'Y' or g == ''):
        try:
            db.delete_account(account.strip())
            print(
                "Successfully deleted '{0}' from the database.".format(account))
        except Error:
            print('An error occurred during database processing. :(')


def edit_mode():
    while(True):
        print('What do you want do you?')
        g = input('(E)dit Password, (D)elete Password, E(x)it: ')
        while(g != 'e' and g != 'E' and g != 'd' and g != 'D' and g != 'x' and g != 'X'):
            g = input('(E)dit Password, (D)elete Password, E(x)it: ')
        if(g == 'e' or g == 'E'):
            edit_password()
        elif(g == 'd' or g == 'D'):
            delete_password()
        elif(g == 'x' or g == 'X'):
            sys.exit(0)
        print('')


if __name__ == "__main__":
    print('\n~*~*~*~*~*~*~*~*~*~*~*~* Alohomora *~*~*~*~*~*~*~*~*~*~*~*~\n')
    if(len(sys.argv) > 1):
        flag = sys.argv[1]
        # if(flag == 'e'):
        edit_mode()
    if(len(sys.argv) <= 1):
        init()
        secret = enter_secret()
        print('\n~*~*~*~*~*~*~*~*~*~* Ready for Sorcery *~*~*~*~*~*~*~*~*~*~\n')
        get_password(secret)

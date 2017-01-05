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
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# ------------------------------------------------------------------------------

# Python
import sys
from os import path

# PIP
import hashlib
import pyperclip
import getpass
import readline

# Alohomora
import add_account
import db
import completer
import delete_account
import edit_account
import pw_gen
import shell_io

# ------------------------------------------------------------------------------


db_file = path.join(path.dirname(
    path.realpath(__file__)), 'database/db.sqlite3')


def init():
    if(not path.isfile(db_file)):
        print('No database was found.')
        print('If you already have a database, move it to \'database/\'.')
        print('If this is the first time you use Alohomora, you can create\n\
a new database.\n')
        print('What do you want me to do?')
        g = shell_io.key_input('(C)reate new one, (E)xit: ', ['c', 'C', 'e', 'E'])
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
        g = shell_io.key_input("ok? (y/n)",
                               ['n', 'N', 'y', 'Y', ''])
        if(g == 'n' or g == 'N'):
            b = False
            print("\n------------------------------\n")
        if(g == 'y' or g == 'Y' or g == ''):
            b = True
    return secret


def get_password(secret):
    accounts = db.get_accounts()
    text_completer = completer.TextCompleter(accounts)
    readline.set_completer(text_completer.complete)
    readline.parse_and_bind('tab: complete')
    while(True):
        account = input("Account: ")
        if(account not in accounts):
            g = shell_io.key_input("'{0}' is not in your database base yet, wanna add it? (y/n)".format(
                account), ['y', 'Y', 'n', 'N', ''], "wanna add it? (y/n)")
            if(g == 'n' or g == 'N'):
                continue
            if(g == 'y' or g == 'Y' or g == ''):
                add_account.add(account)
                text_completer.update(account)
                accounts.append(account)
                print("\n~~~ '{account}' was added to your database ~~~\n".format(
                    account=account))
                print('\n~*~*~*~*~*~*~*~*~*~* Ready for Sorcery *~*~*~*~*~*~*~*~*~*~\n')
        _, _, salt, length, lowercase, uppercase, numbers, specials = db.get_account(
            account)
        password = pw_gen.get_password(
            secret, salt, length, lowercase, uppercase, numbers, specials)
        print(password)
        # print()
        # print('first 5 letters: ' + password[0:5])
        # print('~~~ copied to clipboard ~~~')
        # print("\n------------------------------\n")


def edit_mode():
    while(True):
        print('What do you want do you?')
        g = shell_io.key_input('(E)dit Password, (D)elete Password, E(x)it: ',
                               ['e', 'E', 'd', 'D', 'x', 'X'])
        if(g == 'e' or g == 'E'):
            edit_account.edit()
        elif(g == 'd' or g == 'D'):
            delete_account.delete()
        elif(g == 'x' or g == 'X'):
            sys.exit(0)
        print('')


if __name__ == "__main__":
    print('\n~*~*~*~*~*~*~*~*~*~*~*~* Alohomora *~*~*~*~*~*~*~*~*~*~*~*~\n')
    if(len(sys.argv) > 1):
        flag = sys.argv[1]
        if(flag == '-e'):
            edit_mode()
    if(len(sys.argv) <= 1):
        init()
        secret = enter_secret()
        print('\n~*~*~*~*~*~*~*~*~*~* Ready for Sorcery *~*~*~*~*~*~*~*~*~*~\n')
        get_password(secret)

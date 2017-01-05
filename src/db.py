#!/usr/bin/python3

# ------------------------------------------------------------------------------

# Python
from os import path, makedirs
import sqlite3

# Alohomora
from salt import gen_salt

# ------------------------------------------------------------------------------


db_path = path.join(path.dirname(path.realpath(__file__)), 'database')
db_file = path.join(db_path, 'db.sqlite3')


def init():
    if(not path.exists(db_path)):
        makedirs(db_path)
    con = sqlite3.connect(db_file)
    cur = con.cursor()
    cur.execute("""
CREATE TABLE `accounts` (
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `name` TEXT NOT NULL UNIQUE,
    `salt` TEXT NOT NULL UNIQUE,
    `length` INTEGER NOT NULL,
    `lowercase` TEXT NOT NULL,
    `uppercase` TEXT NOT NULL,
    `numbers` TEXT NOT NULL,
    `specials` TEXT NOT NULL
);""")
    con.commit()
    con.close()


def get_account(name):
    con = sqlite3.connect(db_file)
    cur = con.cursor()
    cur.execute("Select * from accounts Where name = '{0}'".format(name))
    accounts = cur.fetchall()
    con.close()
    return accounts[0]


def get_accounts():
    con = sqlite3.connect(db_file)
    cur = con.cursor()
    cur.execute("Select name from accounts")
    accounts = cur.fetchall()
    con.close()
    return [row[0] for row in accounts]


def get_accounts_detailed():
    con = sqlite3.connect(db_file)
    cur = con.cursor()
    cur.execute("SELECT * FROM accounts")
    accounts = cur.fetchall()
    con.close()
    return accounts


def add_account(name, length, lowercase, uppercase, numbers, specials):
    con = sqlite3.connect(db_file)
    cur = con.cursor()
    salt = gen_salt()
    try:
        cur.execute("""
INSERT INTO accounts (name, salt, length, lowercase, uppercase, numbers,
    specials)
    VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}')"""
                    .format(name, salt, length, lowercase, uppercase, numbers,
                            specials))
        con.commit()
    except sqlite3.IntegrityError as e:
        print("{name} is already in the database".format(name=name))
    con.close()


def delete_account(name):
    con = sqlite3.connect(db_file)
    cur = con.cursor()
    cur.execute("DELETE FROM accounts WHERE name = '{0}'".format(name))
    con.commit()
    con.close()


def update_length(name, length):
    con = sqlite3.connect(db_file)
    cur = con.cursor()
    cur.execute(
        "UPDATE accounts SET length = {0} WHERE name = '{1}'".format(length, name))
    con.commit()
    con.close()


def update_salt(name):
    salt = gen_salt()
    con = sqlite3.connect(db_file)
    cur = con.cursor()
    cur.execute(
        "UPDATE accounts SET salt = '{0}' WHERE name = '{1}'".format(salt, name))
    con.commit()
    con.close()


def update_character_sets(name, lowercase, uppercase, numbers, specials):
    salt = gen_salt()
    con = sqlite3.connect(db_file)
    cur = con.cursor()
    cur.execute("""UPDATE accounts
    SET lowercase = '{0}',
        uppercase = '{1}',
        numbers = '{2}',
        specials = '{3}'
    WHERE name = '{4}'""".format(lowercase, uppercase, numbers, specials, name))
    con.commit()
    con.close()

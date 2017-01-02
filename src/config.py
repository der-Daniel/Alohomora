#!/usr/bin/python3

# ------------------------------------------------------------------------------

# Python
from os import path
import sys

# Alohomora
import configparser as cp

# ------------------------------------------------------------------------------


config_file = path.join(path.dirname(
    path.realpath(__file__)), 'config.ini')


def get_settings():
    ini = cp.ConfigParser()
    ini.read(config_file)
    s = None
    try:
        s = ini['password']
    except KeyError:
        print("'password' section not found.")
        sys.exit(0)
    length = 0
    try:
        length = int(s.get('length'))
    except ValueError:
        print("config.ini: length is not an integer")
    lowercase = s.get("lowercase")
    if(lowercase is None):
        print("config.ini: lowercase is missing")
        sys.exit(0)
    uppercase = s.get("uppercase")
    if(uppercase is None):
        print("config.ini: uppercase is missing")
        sys.exit(0)
    numbers = s.get("numbers")
    if(numbers is None):
        print("config.ini: numbers is missing")
        sys.exit(0)
    specials = s.get("specials")
    if(specials is None):
        print("config.ini: specials is missing")
        sys.exit(0)
    return length, lowercase, uppercase, numbers, specials

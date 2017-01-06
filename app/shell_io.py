#!/usr/bin/python3

# ------------------------------------------------------------------------------

# Python
import re

# Pip
import readline

# ------------------------------------------------------------------------------


def parameter_input(prompt, prefill=''):
    readline.set_startup_hook(lambda: readline.insert_text(str(prefill)))
    try:
        return input(prompt)
    finally:
        readline.set_startup_hook()


def key_input(prompt, keys, second_prompt=None):
    a = input(prompt)
    while(a not in keys):
        if(second_prompt is None):
            a = input(prompt)
        else:
            a = input(second_prompt)
    return a


def get_length(length):
    length = parameter_input("Length: ", length).strip()
    while(True):
        try:
            length = int(length)
        except ValueError:
            print('length must be an integer')
            length = input('Length: ')
            continue
        if(length < 1):
            print('length must be a positive integer')
            length = input('Length: ')
            continue
        break
    return length


def get_lowercase(lowercase):
    lowercase = parameter_input("Lowercase: ", lowercase).strip()
    while(len(re.findall(r"[a-z]", lowercase)) != len(lowercase)):
        print('Only lowercase letters are allowed.')
        lowercase = input("lowercase: ").strip()
    return lowercase


def get_uppercase(uppercase):
    uppercase = parameter_input("Uppercase: ", uppercase).strip()
    while(len(re.findall(r"[A-Z]", uppercase)) != len(uppercase)):
        print('Only uppercase letters are allowed.')
        uppercase = input("uppercase (type 'A-Z' for default): ").strip()
    return uppercase


def get_numbers(numbers):
    numbers = parameter_input("Numbers: ", numbers).strip()
    while(len(re.findall(r"[0-9]", numbers)) != len(numbers)):
        print('Only numbers are allowed.')
        numbers = input("numbers: ").strip()
    return numbers


def get_specials(specials):
    specials = parameter_input("Specials: ", specials).strip()
    return specials

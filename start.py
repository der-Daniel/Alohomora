#!/usr/bin/python3

import argparse
import os
from app import alohomora

parser = argparse.ArgumentParser(description='Alohomora is a free and open source password manager, that does NOT store any passwords at any time')
parser.add_argument('-e', '--edit-mode', help='enter edit mode', action='store_true')

if __name__ == "__main__":
    args = parser.parse_args()
    os.system('cls||clear')
    alohomora.start(args.edit_mode)

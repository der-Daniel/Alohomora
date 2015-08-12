#!/usr/bin/python

# ------------------------------------------------------------------------------

# imports
import sys
import optparse
import binascii as decoder
import getpass
# dependency import
# passlib
# license: BSD license
# https://code.google.com/p/passlib/
from passlib.utils import pbkdf2 as crpyto
# pyperclip
# license: https://github.com/asweigart/pyperclip/blob/master/LICENSE.txt
# https://github.com/asweigart/pyperclip
import pyperclip

# ------------------------------------------------------------------------------




"""
derivePassword

derives a key via a PBKDF2 implementation of passlib
is uses sha-512 as pseudo random function

"""
def derivePassword(secret, salt, iterations=10000, length=64, algorithm='hmac-sha384'):
    pw = decoder.hexlify(crpyto.pbkdf2(secret, salt, iterations, length, algorithm))
    copyToClipboard(pw)
    return pw.decode('utf-8')


"""
copyToClipboard

copy the pw to the system's clipboard

"""
def copyToClipboard(pw):
    pyperclip.copy(pw)



"""
prettyPrint

adds line reak after every 20th character

"""
def prettyPrint(pw):
    lines = [pw[i:i+20] for i in range(0, len(pw), 20)]
    prettypw = ""
    for line in lines:
        prettypw = prettypw + "\n" + line if prettypw != "" else line
    print("\nkey:")
    print("--------------------")
    print(prettypw)
    print("--------------------")
    print("copied to clipboard\n")


"""
main method

possible arugments:
interations: Number of iterations of the underlying pseudo-random function
length: Length of the generated hash

"""
if __name__ == "__main__":
    parser = optparse.OptionParser("usage: alohomora.py [options]")
    parser.add_option("-i", "--iterations", dest="iterations", default="10000", type="int", help="Number of iterations of the underlying pseudo-random function")
    parser.add_option("-l", "--length", dest="length", default="64", type="int", help="Length of the generated hash")
    parser.add_option("-a", "--algorithm", dest="algorithm", default="hmac-sha512", type="string", help="Underlying pseudo-random function: 'hmac-sha1', 'hmac-sha256', 'hmac-sha384', 'hmac-sha512'")
    (options, args) = parser.parse_args()
    secret = getpass.getpass("Enter your Secret: ")
    salt = input("Enter a Salt: ")
    prettyPrint(derivePassword(bytes(secret, 'utf-8'), bytes(salt, 'utf-8'), options.iterations, options.length, options.algorithm))

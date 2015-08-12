#!/usr/bin/env python

# ------------------------------------------------------------------------------

# Copyright reference for passlib

# Passlib
# Copyright (c) 2008-2012 Assurance Technologies, LLC.
# All rights reserved.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


# Copyright reference for pyperclip

# pyperclip
# Copyright (c) 2014, Al Sweigart
# All rights reserved.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# ------------------------------------------------------------------------------

# imports

from passlib.utils import pbkdf2 as crpyto
import pyperclip

import sys
import os
import optparse
import getpass
import binascii as decoder
import hashlib
import completer
import readline
import configparser

# ------------------------------------------------------------------------------




"""
derive_password

derives a key via a PBKDF2 implementation of passlib

"""
def derive_password(secret, salt, iterations=2901, length=20, algorithm='hmac-sha1'):
    pw = decoder.hexlify(crpyto.pbkdf2(secret, salt, iterations, length, algorithm))
    return pw.decode('utf-8')


"""
copy_to_clipboard

copys the pw to the system's clipboard

"""
def copy_to_clipboard(pw):
    pyperclip.copy(pw.decode('utf-8'))


"""
save_service

adds a new service to the txt file

"""
def save_service(service):
    service_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'services.txt')
    with open(service_path, 'a') as f:
        f.write(service + '\n')


"""
main method

interactive shell app

"""
if __name__ == "__main__":
    src_path = os.path.dirname(os.path.realpath(__file__))
    config_path = os.path.join(src_path, 'config.ini')
    config = configparser.RawConfigParser()
    if(not os.path.isfile(config_path)):
        raise OSError(2, 'No such file or directory', 'config.ini')
    config.read(config_path)
    params = dict(config.items('pbkdf'))
    print('\n~*~*~*~*~*~*~*~*~*~*~*~* Alohomora *~*~*~*~*~*~*~*~*~*~*~*~\n')
    b = False
    while(not b):
        secret = getpass.getpass("Enter your Secret: ")
        fingerprint = hashlib.sha1(secret.encode('utf-8')).hexdigest()
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
    print('\n~*~*~*~*~*~*~*~*~*~* Ready for Sorcery *~*~*~*~*~*~*~*~*~*~\n')
    service_path = os.path.join(src_path, 'services.txt')
    if(not os.path.isfile(service_path)):
        raise OSError(2, 'No such file or directory', 'services.txt')
    services = open(service_path).read().splitlines()
    text_completer = completer.TextCompleter(services)
    readline.set_completer(text_completer.complete)
    readline.parse_and_bind('tab: complete')  
    while(True):
        salt = input("Enter a Salt: ")
        if(salt not in services):
            g = input("'" + salt + "' is not in your database base yet, wanna add it? (y/n)")
            while(g != 'n' and g != 'N' and g != 'y' and g != 'Y' and g != ''):
                g = input("wanna add it? (y/n)")
            if(g == 'y' or g == 'Y' or g == ''):
                save_service(salt)
                text_completer.update(salt)
                services.append(salt)
                print("~~~ '" + salt + "' was added to your database ~~~")
            if(g == 'n' or g == 'N'):
                print("~~~ '" + salt + "' is used just this time ~~~")
        password = derive_password(bytes(secret, 'utf-8'), bytes(salt, 'utf-8'), int(params['iterations']), int(params['length']), params['algorithm'])
        pyperclip.copy(password)
        print()
        print('first 5 letters: ' + password[0:5])
        print('~~~ copied to clipboard ~~~')
        print("\n------------------------------\n")

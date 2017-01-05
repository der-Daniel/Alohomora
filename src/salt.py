#!/usr/bin/python3

# ------------------------------------------------------------------------------

# Python
import os
import binascii

# ------------------------------------------------------------------------------


def gen_salt(length=512):
    uran = os.urandom(length)
    return binascii.hexlify(uran).decode('utf-8')

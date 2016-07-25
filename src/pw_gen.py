#!/usr/bin/python3

# Copyright reference for passlib

# Passlib
# Copyright (c) 2008-2012 Assurance Technologies, LLC.
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

# imports

from math import ceil, log
import re
from passlib.utils import pbkdf2
from bitstring import BitString as bit

# ------------------------------------------------------------------------------


def pbkdf(secret, salt):
    password = pbkdf2.pbkdf2(bytes(secret, 'utf-8'), bytes(salt, 'utf-8'), 15000, 512, 'hmac-sha512')
    return password


def verify(pw, lowercase, uppercase, numbers, specials):
    correct = True
    if(lowercase):
        correct &= re.search(r"[{0}]".format(lowercase), pw) is not None
    if(uppercase):
        correct &= re.search(r"[{0}]".format(uppercase), pw) is not None
    if(numbers):
        correct &= re.search(r"[{0}]".format(numbers), pw) is not None
    if(specials):
        correct &= re.search(r"[{0}]".format(specials), pw) is not None
    return correct


def get_password(secret, salt, pw_len, lowercase, uppercase, numbers,
                 specials):
    raw = pbkdf(secret, salt)
    alphabet = lowercase + uppercase + numbers + specials
    alpha_len = len(alphabet)
    bits_per_char = ceil(log(alpha_len) / log(2))
    i = 1
    password = ''
    while(verify(password, lowercase, uppercase, numbers, specials) is False):
        random_bits = bit(bytes=raw)[0:i * 100 + pw_len * bits_per_char]
        n = random_bits.int % (pow(pow(2, bits_per_char), pw_len))
        bits = bit(hex=hex(n))
        password = ''
        for j in range(0, pw_len):
            n = j * bits_per_char
            m = (j + 1) * bits_per_char
            password += alphabet[bits[n:m].uint % alpha_len]
        i += 1
    return password

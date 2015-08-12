# Alohomora with Python
### Alohomora is a free and open source password manager
**It is published under the GNU General Public License**  


Alohomora is pure magic. It remembers all of your secret passwords without ever storing any of them. How? Well, it uses [**Password-Based Key Derivation Function (PBKDF)**](https://en.wikipedia.org/wiki/PBKDF2) to derive passwords just at runtime.  No Eve will ever be able to steal anything, since there never is a file.  

## Scheme

PBKDFs are deterministic hash functions. Deterministic means, that whenever you put the same arguments into them, the result will be the same. In our scenario it comes down to 2 important arguments: Your secret and a word.  

Let's assume your secret is 'asdfg' and other word is 'twitter.com'. So whenever you put 'asdfg' and 'twitter.com' into a PBKDF the result will be the same. If you change 'twitter.com' to 'gmail.com' the result will be different, but deterministically be the same each time you enter 'asdfg' and 'gmail.com'. 
With this scheme you can address all your web services by simply using the service's name. All you need to remember within this procedure is your secret.

PBKDFs guarantees that an output cannot be inverted, even if an attacker knew which service name you had used. 

<br>


## Dependencies

- [**Python 3.4.3**](https://www.python.org/downloads/release/python-343/)  (or higher)

- [**Passlib**](http://passlib.googlecode.com/)  
Python lib that implements PBKDF2  
install via pip:
`pip install passlib`  
published under [BSD license](http://opensource.org/licenses/BSD-3-Clause)

- [**Pyperclip**](https://github.com/asweigart/pyperclip)  
Python lib to copy text into the clipboard  
install via pip:
`pip install pyperclip`  
published under [BSD license](https://github.com/asweigart/pyperclip/blob/master/LICENSE.txt)
<br>

## Installation

Clone this repository. 
Execute `/src/alohomora.py` from your shell.


<br>

## Usage / Example  

**i. Start App**
**`$python alohomora.py`**  
```
~*~*~*~*~*~*~*~*~*~*~*~* Alohomora *~*~*~*~*~*~*~*~*~*~*~*~

Enter your Secret: 
```

**ii. Enter your secret**

```

fingerprint:
-------------------
ff69c782303c0074dc4
54a96426f9721b39d58
-------------------

ok? (y/n)
```

**iii. check the fringerprint**  
**iv. enter a web service**

```

~*~*~*~*~*~*~*~*~*~* Ready for Sorcery *~*~*~*~*~*~*~*~*~*~

Enter a Salt: github.com

```

**v. the derived password is copied to the clipboard**

```

first 5 letters: d8814
~~~ copied to clipboard ~~~

------------------------------
```


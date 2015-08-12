# Alohomora with Python
### Alohomora is a free and open source password manager
**It is published under the GNU General Public License**  


Alohomora remembers all your passwords **without** any database or storing routine. This **significantly** enhance data security, since there is no physical database, file or something else an attacker could steal. Moreover you do not rely on any stakeholder, you need to trust in *managing* your passwords.  

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
published under [this license](https://github.com/asweigart/pyperclip/blob/master/LICENSE.txt)
<br>

## Installation

Clone this repository. Add `[...]/Alohomoa/src` to your path variable.  
You should be able to call `alohomora.py` from your shell now.  


<br>

## Usage  

- **`python alohomora.py --help`**  

```bash
Usage: alohomora.py [options]

Options:
  -h, --help            show this help message and exit
  -i ITERATIONS, --iterations=ITERATIONS
                        Number of iterations of the underlying pseudo-random
                        function
  -l LENGTH, --length=LENGTH
                        Length of the generated hash
  -a ALGORITHM, --algorithm=ALGORITHM
                        Underlying pseudo-random function: 'hmac-sha1', 'hmac-
                        sha256', 'hmac-sha384', 'hmac-sha512'
```

- **`python alohomora.py`**

```bash
Enter your Secret:
Enter a Salt: twitter.com

key:
++++++++++++++++++++
bb0d1fffc676d8d0240a
bbaa704517e40f4ea8f4
ae6f4e03525c40db4427
6886505458af6383545c
43e60acecefa8bb629e7
b5cef6737aa02bd0e1ff
ec92950d
++++++++++++++++++++
copied to clipboard
```

- **`python alohomora.py -i 1337 -l 42`**  
```bash
Enter your Secret:
Enter a Salt: twitter.com

key:
++++++++++++++++++++
69fb6d93fbbecba1f552
62e00bad0582ec62954c
63accbf6d2bdf0aa8fdb
8d1c4e8a062f04bcd99c
0b2b
++++++++++++++++++++
copied to clipboard
```

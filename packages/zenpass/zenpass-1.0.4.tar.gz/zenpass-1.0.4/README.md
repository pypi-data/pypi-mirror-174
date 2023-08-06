# Zenpass

[![PyPI](https://img.shields.io/pypi/v/zenpass)](https://pypi.python.org/pypi/zenpass)
[![Pypi - License](https://img.shields.io/github/license/codesrg/zenpass)](https://github.com/codesrg/zenpass/blob/main/LICENSE)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/zenpass?color=red)](https://pypi.python.org/pypi/zenpass)

To generate random and strong passwords.

## Installation

`pip install -U zenpass`

## Usage

```
usage: zenpass [options]

optional arguments:
  -h, --help         show this help message and exit
  -v, --version      show version number and exit.

to customize Password:
  -l , --length      to set length to the password
  -n , --ignore      to ignore unwanted characters to the password
  -i , --include     to include characters to the password
  -o , --only        to create password only using wanted characters
  -s , --separator   the separator character
  -c , --seplen      the length of characters between separator
  --repeat           to repeat the characters in the password (default : False)
  --separation       to separate password characters using separator (default : False)
  --show             to show password (default : False)
```

###
To generate a random password.
```
$ zenpass
Password copied to clipboard.
```
###

To set the password length, Default password length is `8-16`.

```
$ zenpass -l 10 --show
Password: Q3m/vro|uR
Password copied to clipboard.
```
###

Whether the characters in passwords repeat or not,
Default value of `repeat` is `False`.
```
$ zenpass -r --show
Password: 96Ndl;1D$jQu4Z2
Password copied to clipboard.
```
###

To include, ignore or use only `'alphabets'`, `'numbers'`, `'uppercase'`, `'lowercase'`, `'symbols'` and `random characters` in generating password.
###

To ignore `numbers` in passwords. 

```
$ zenpass -n numbers --show
Password: uyMXP‘$!ZSCYqzj
Password copied to clipboard.
```
###
To ignore characters `a,b,c,d,e`
```
$ zenpass -n abcde --show
Password: ~}t"R‘jF'ksG8~E
Password copied to clipboard.
```
###
To create a password only using `special characters`.

```
$ zenpass -o symbols -l 15 --show
Password: ?)".=-_^[_‘~{.)
Password copied to clipboard.
```
###
To include `a,b,c,d,e` characters in a password.
```
$ zenpass -o numbers -i abcde -l 15 --show
Password: 78713d1e3d926a3
Password copied to clipboard.
```
###
To separate characters in a password using separator.
```
$ zenpass -o uppercase --separation -l 16 --show
Password: YNQC-RKBF-DMAT-UVIP
Password copied to clipboard.
```
###
To separate characters in a password using separator `_` with `5` characters between each separator.
```
$ zenpass -o uppercase --separation -l 15 -s _ -c 5 --show
Password: YNQCR_KBFDM_ATUVI
Password copied to clipboard.
```

## Issues:

If you encounter any problems, please file an [issue](https://github.com/codesrg/zenpass/issues) along with a detailed description.
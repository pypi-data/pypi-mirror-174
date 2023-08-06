# Sipher

[![PyPI](https://img.shields.io/pypi/v/sipher)](https://pypi.python.org/pypi/sipher)
[![Pypi - License](https://img.shields.io/github/license/codesrg/sipher)](https://github.com/codesrg/sipher/blob/main/LICENSE)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/sipher?color=red)](https://pypi.python.org/pypi/sipher)

To encrypt and decrypt message. 

Only morse encryption/decryption is supported.

## Installation

`pip install -U sipher`

## Usage

```
usage: sipher [options]

optional arguments:
  -h, --help     show this help message and exit
  -v, --version  show version number and exit.

to encrypt/decrypt message:
  data           data to encrypt/decrypt
  -e, --encrypt  to encrypt message
  -d, --decrypt  to decrypt message
  -c, --copy     to copy encrypted/decrypted message to clipboard (default :
                 False)
  -s, --store    to store encrypted/decrypted message as text file (default :
                 False)
  -p, --path     path to store encrypted/decrypted message
```

###
To encrypt a text and copy it to clipboard.
```
$ sipher data --encrypt --copy
Encrypted message copied to clipboard.
```
###

To decrypt a cipher and store it as text file.

```
$ sipher "-.. .- - .- " --decrypt --store
Encrypted message copied to clipboard.
Encrypted message stored in 'path_given'.
```

## Issues:

If you encounter any problems, please file an [issue](https://github.com/codesrg/sipher/issues) along with a detailed description.
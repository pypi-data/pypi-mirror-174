import argparse
import os

from sipher.morse import Morse

__prog__ = 'sipher'
__version__ = '1.0.1'


def get_argument():
    parser = argparse.ArgumentParser(prog=__prog__, usage="sipher [options]")
    parser.add_argument('-v', '--version', action='version', help='show version number and exit.', version=__version__)
    group = parser.add_argument_group("to encrypt/decrypt message")
    group.add_argument("data", type=str, help="data to encrypt/decrypt")
    group.add_argument("-e", "--encrypt", dest="encrypt", default=False, action="store_true",
                       help="to encrypt message")
    group.add_argument("-d", "--decrypt", dest="decrypt", default=False, action="store_true",
                       help="to decrypt message")
    group.add_argument("-c", "--copy", dest="copy_to_clipboard", default=False, action="store_true",
                       help="to copy encrypted/decrypted message to clipboard (default : %(default)s)")
    group.add_argument("-s", "--store", dest="store", default=False, action="store_true",
                       help="to store encrypted/decrypted message as text file (default : %(default)s)")
    group.add_argument("-p", "--path", dest="store_path", default=os.getcwd(), metavar='',
                       help="path to store encrypted/decrypted message")
    parser.add_argument_group(group)
    options = parser.parse_args()
    if not options.encrypt and not options.decrypt:
        parser.error("one of the following arguments are required: -e/--encrypt or -d/--decrypt")
    if options.encrypt and options.decrypt:
        parser.error("any one of the following arguments should be given: -e/--encrypt or -d/--decrypt")
    if not options.copy_to_clipboard and not options.store:
        parser.error("one of the following arguments are required: -c/--copy or -s/--store")
    return options


def encrypt(m: Morse, data: str, copy_to_clipboard: bool = False, store: bool = False, store_path: str = None):
    m.encrypt(data=data, copy_to_clipboard=copy_to_clipboard, store=store, store_path=store_path)


def decrypt(m: Morse, data: str, copy_to_clipboard: bool = False, store: bool = False, store_path: str = None):
    m.decrypt(data=data, copy_to_clipboard=copy_to_clipboard, store=store, store_path=store_path)


def main():
    options = get_argument()
    m = Morse()
    if options.encrypt:
        encrypt(m, options.data, options.copy_to_clipboard, options.store, options.store_path)
    elif options.decrypt:
        decrypt(m, options.data, options.copy_to_clipboard, options.store, options.store_path)


if __name__ == "__main__":
    main()

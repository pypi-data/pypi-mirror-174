from __future__ import annotations

import calendar
from datetime import datetime
import os
import pyperclip
from os import PathLike
from pathlib import Path
from typing import AnyStr, Optional


class Morse:
    def __init__(self):
        self.__MORSE_CODE = {'A': '.-', 'B': '-...',
                             'C': '-.-.', 'D': '-..', 'E': '.',
                             'F': '..-.', 'G': '--.', 'H': '....',
                             'I': '..', 'J': '.---', 'K': '-.-',
                             'L': '.-..', 'M': '--', 'N': '-.',
                             'O': '---', 'P': '.--.', 'Q': '--.-',
                             'R': '.-.', 'S': '...', 'T': '-',
                             'U': '..-', 'V': '...-', 'W': '.--',
                             'X': '-..-', 'Y': '-.--', 'Z': '--..',
                             '1': '.----', '2': '..---', '3': '...--',
                             '4': '....-', '5': '.....', '6': '-....',
                             '7': '--...', '8': '---..', '9': '----.',
                             '0': '-----', ', ': '--..--', '.': '.-.-.-',
                             '?': '..--..', '/': '-..-.', '-': '-....-',
                             '(': '-.--.', ')': '-.--.-', ' ': ''}
        self.__em = ''
        self.__dm = ''

    def encrypt(self, data: AnyStr | PathLike[AnyStr] = None, copy_to_clipboard: bool = False, store: bool = False,
                store_path: Optional[str] = None):
        for letter in data:
            self.__em += self.__MORSE_CODE[letter.upper()] + " "
        if copy_to_clipboard is True:
            pyperclip.copy(self.__em)
            if pyperclip.paste() == self.__em:
                print("Encrypted message copied to clipboard.")
        if store is True:
            path = self.__store(self.__em, store_path)
            if path.exists():
                print("Encrypted message stored in '" + path.__str__() + "'")
        return self.__em

    def decrypt(self, data: AnyStr | PathLike[AnyStr] = None, copy_to_clipboard: bool = False, store: bool = False,
                store_path: Optional[str] = None):
        word_list = [word for word in data.split("  ")]
        for word in word_list:
            for char in word.split():
                index = list(self.__MORSE_CODE.values()).index(char)
                self.__dm += list(self.__MORSE_CODE.keys()).pop(index)
            self.__dm += " "
        self.__dm = self.__dm.strip()
        if copy_to_clipboard is True:
            pyperclip.copy(self.__dm)
            if pyperclip.paste() == self.__dm:
                print("Decrypted message copied to clipboard.")
        if store is True:
            path = self.__store(self.__dm, store_path)
            if path.exists():
                print("Decrypted message stored in '" + path.__str__() + "'")
        return self.__dm

    @staticmethod
    def __store(data: str, path: Optional[str]):
        if not path:
            path = os.getcwd()
        path += "/morse_" + str(calendar.timegm(datetime.now().timetuple())) + ".txt"
        path = Path(path)
        with open(path, "w") as morse_file:
            morse_file.write(data)
        return path

import random

from . import constant as pc
from .exception import ZenpassException


class PasswordGenerator:
    def __init__(self, length: int = None, ignore: str = None, only: str = None, include: str = None,
                 repeat: bool = False, separator: str = None, separator_length: int = None, separation: bool = False):
        self.__password = None
        self.__available_char = None
        self.__possibility = None
        self.length = length if length is not None else False
        self.ignore = ignore if ignore is not None else False
        self.only = only if only is not None else False
        self.include = include if include is not None else False
        self.repeat = repeat
        self.separator_length = separator_length if separator_length is not None else False
        self.separator = separator if separator else separation

    def __all_possible_chars(self) -> None:
        self.__possibility = pc.POSSIBLE_UPPERCASE_CHARS + pc.POSSIBLE_LOWERCASE_CHARS + pc.POSSIBLE_NUMBERS \
                             + pc.POSSIBLE_SPECIAL_CHARS
        self.__available_char = {
            "alphabets": pc.POSSIBLE_UPPERCASE_CHARS + pc.POSSIBLE_LOWERCASE_CHARS,
            "uppercase": pc.POSSIBLE_UPPERCASE_CHARS,
            "lowercase": pc.POSSIBLE_LOWERCASE_CHARS,
            "numbers": pc.POSSIBLE_NUMBERS,
            "symbols": pc.POSSIBLE_SPECIAL_CHARS
        }

    def __set_length(self) -> None:
        if not self.length:
            if not self.only:
                self.length = random.randint(pc.DEFAULT_MIN_PASS_LEN,
                                             pc.DEFAULT_MAX_PASS_LEN)
            else:
                raise ZenpassException('[-] Password length must be given.')

    def __add_only_wanted(self) -> None:
        possibility = pc.EMPTY_STRING
        try:
            choices = [character for character in str(self.only).split(',')]
            for choice in choices:
                if choice.lower() in self.__available_char:
                    possibility += self.__available_char[choice.lower()]
                if not choice.lower() in self.__available_char:
                    for char in choice:
                        possibility += char
        except Exception:
            raise ZenpassException
        self.__possibility = possibility

    def __remove_unwanted(self) -> None:
        try:
            choices = [characters for characters in str(self.ignore).split(',')]
            if self.ignore == ',' or ',,,' in self.ignore or ',,' in self.ignore or len(choices) > 0:
                possibility = self.__possibility.replace(',', pc.EMPTY_STRING)
                for choice in choices:
                    if choice.lower() in self.__available_char:
                        for char in self.__available_char[choice.lower()]:
                            possibility = possibility.replace(char, pc.EMPTY_STRING)
                    if choice not in self.__available_char:
                        for char in choice:
                            possibility = possibility.replace(char, pc.EMPTY_STRING)
                self.__possibility = possibility
        except Exception:
            raise ZenpassException

    def __include_characters(self) -> None:
        possibility = self.__possibility
        try:
            choices = [character for character in str(self.include).split(',')]
            for choice in choices:
                if choice.lower() in self.__available_char:
                    for char in self.__available_char[choice.lower()]:
                        if char not in possibility:
                            possibility += char
                if not choice.lower() in self.__available_char:
                    for char in choice:
                        if char not in possibility:
                            possibility += char
        except Exception:
            raise ZenpassException
        self.__possibility = possibility

    def __repeat_char(self) -> None:
        if self.repeat is None or self.repeat is True:
            self.__possibility *= self.length

    def __check(self) -> None:
        if self.length and ((self.length > len(
                self.__possibility)) or self.length > pc.PASSWORD_LENGTH_LIMIT):
            raise ZenpassException('[-] Password length must be less.')

    def __separated_pass(self) -> str:
        if type(self.separator) is bool:
            self.separator = pc.DEFAULT_SEPARATOR
        if not self.separator_length:
            self.separator_length = pc.DEFAULT_SEPARATE_LENGTH
        final_password = pc.EMPTY_STRING
        for i in range(len(self.__password)):
            if i % self.separator_length == 0 and i != 0:
                final_password += self.separator + self.__password[i]
            else:
                final_password += self.__password[i]
        return final_password

    def __filter(self) -> None:
        if self.only:
            self.__add_only_wanted()
        if self.include:
            self.__include_characters()
        if self.ignore:
            self.__remove_unwanted()
        self.__repeat_char()

    def generate(self) -> str:
        self.__all_possible_chars()
        self.__set_length()
        self.__filter()
        self.__check()
        self.__password = pc.EMPTY_STRING.join(random.sample(self.__possibility, self.length))
        return self.__separated_pass() if self.separator or self.separator_length else self.__password

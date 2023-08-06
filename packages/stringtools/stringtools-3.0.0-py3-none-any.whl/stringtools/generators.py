# MIT License

# Copyright (c) 2022 Beksultan Artykbaev

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import string
import random
import secrets
from abc import ABC, abstractmethod
from typing import List, Tuple, Union


class Sounds:
	vowels = [
		"a",
		"e",
		"i",
		"o",
		"u",
		"eir",
		"ay",
		"eau",
		"au",
		"ayer",
		"ei",
		"igh",
		"aw",
		"ow",
		"ore",
		"ou",
		"er",
		"ae",
		"augh",
		"ough",
		"oo",
		"uoy",
		"oar",
		"our",
		"eer",
		"et",
		"eigh",
		"ey",
		"ye",
		"ai",
		"ew",
		"eo",
		"uy",
		"u",
		"air",
		"oew",
		"oa",
		"ur",
		"oe",
		"ie",
		"are",
		"ir",
		"ea",
		"oy",
		"aigh",
		"or",
		"ui",
		"yr",
		"ar",
		"oor",
		"ier",
		"ue",
		"ee",
		"oi",
		"ear",
		"ho",
		"ure",
		"is",
		"ere",
	]
	consonants = [
		"b",
		"c",
		"d",
		"f",
		"g",
		"h",
		"j",
		"k",
		"l",
		"m",
		"n",
		"p",
		"q",
		"r",
		"s",
		"t",
		"v",
		"w",
		"x",
		"y",
		"z",
		"rr",
		"sh",
		"th",
		"gu",
		"zz",
		"ff",
		"sc",
		"ft",
		"dd",
		"wr",
		"tt",
		"tu",
		"qu",
		"rh",
		"ss",
		"bb",
		"lm",
		"pn",
		"pp",
		"lf",
		"se",
		"mn",
		"ti",
		"ll",
		"ph",
		"ps",
		"te",
		"kn",
		"ch",
		"mm",
		"ck",
		"gh",
		"gn",
		"wh",
		"ed",
		"mb",
		"sci",
		"si",
		"dge",
		"ve",
		"ce",
		"cc",
		"ge",
		"st",
		"lk",
		"gg",
		"tch",
		"ze",
		"gue",
		"nn",
		"ci",
		"di",
	]
	def __init__(self) -> None:
		pass

class TextGenerator(ABC):
	'''Abstract class to define TextGenerator classes.'''

	def __init__(self) -> None:
		super().__init__()

	@abstractmethod
	def generate(self) -> str: ...

	@abstractmethod
	def set_length(self): ...


class Nick(Sounds, TextGenerator):
	'''Generate nicknames using vowel and consonant graphemes.'''
	def __init__(self) -> None:
		self.nickname = ""
		self.length = 5
		self.previous_char = ""

	def generate(self, Capitalize: bool = True) -> str:
		self.nickname = ""
		self.previous_char = ""
		if self.length == 0:
			return ""
		while len(self.nickname) != self.length:
			self.nickname += self.__new_char()

		if Capitalize is True:
			return self.nickname.capitalize()
		else:
			return self.nickname

	def set_length(self, length: int):
		'''Sets the length of nickname.'''
		self.length = length

	def __exclude(self, l: List, max_str_len_num: int) -> List:
		# Deletes strings from List if length is higher than max_str_len_num
		if len(l) == 1 and len(l[0]) < max_str_len_num:
			return l
		elif len(l) == 1 and len(l[0]) > max_str_len_num:
			raise ValueError(f"{l} doesn't contain elements with the the length of {max_str_len_num}.")

		return list(filter(lambda a: len(a) <= max_str_len_num, l))

	def __new_char(self) -> str:
		current_len = len(self.nickname)
		max_limit = self.length - current_len
		limited_vowels = self.__exclude(self.vowels, max_limit)
		limited_consonants = self.__exclude(self.consonants, max_limit)
		if max_limit == 0:
			return ""
		if self.previous_char == "":
			char = random.choice(limited_consonants + limited_vowels)
			self.previous_char = char
			return char
		elif self.previous_char in self.vowels:
			char = random.choice(limited_consonants)
			self.previous_char = char
			return char

		elif self.previous_char in self.consonants:
			char = random.choice(limited_vowels)
			self.previous_char = char
			return char

class Password(TextGenerator):
	'''Generate strong passwords.'''
	def __init__(self) -> None:
		self.letters = ""
		self.uppercase = True
		self.lowercase = True
		self.length = 12

	def generate(self) -> str:
		password = ""
		self.letters = "".join(set(self.letters))
		try:
			for i in range(self.length):
				password += self.__upper_lower(secrets.choice(self.letters))
		except IndexError:
			raise ValueError(
				"Please use methods of class first, such as Password.add_digits, Password.add_ascii_letters, e.t.c."
			)
		return password

	def add_digits(self):
		self.letters += string.digits

	def add_ascii_letters(self):
		self.letters += string.ascii_lowercase

	def add_symbols(self):
		self.letters += string.punctuation

	def add_own(self, symbols: Union[str, List, Tuple]):
		self.letters += "".join(symbols)

	def set_length(self, length: int):
		self.length = length

	def exclude_similar(
		self, similar_chars: Union[str, List] = ["1", "L", "O", "0", '"', "'", "I", "b", "6", "|"]):
		'''Excludes similar chars when generating password.'''
		for char in similar_chars:
			self.letters = self.letters.replace(char, "")

	def use_uppercase(self, b: bool):
		self.uppercase = b

	def use_lowercase(self, b: bool):
		self.lowercase = b

	def __upper_lower(self, char: str) -> str:
		'''Checking for upper and lowercase boolean values, and returning character based on input values'''
		if self.lowercase and self.uppercase:
			return secrets.choice([char.lower(), char.upper()])
		elif self.lowercase and not self.uppercase:
			return char.lower()
		elif self.uppercase and not self.lowercase:
			return char.upper()
		elif not self.lowercase and not self.uppercase:
			return char

	@staticmethod
	def __is_symbol(char: str) -> bool:
		if char in string.punctuation:
			return True
		else:
			return False

	@classmethod
	def is_strong(cls, password: str) -> bool:
		'''Checks if password is strong. (Performs below conditions.)
		- If the length is >= 12
		- If it has upper and lowercases
		- If it has at least 1 punctuation symbol, 1 digit, 1 alphabetic character'''
		if len(password) < 12:
			return False
		elif any(char.isdigit() for char in password) is False:
			return False
		elif any(char.isalpha() for char in password) is False:
			return False
		elif any(cls.__is_symbol(char) for char in password) is False:
			return False
		elif password.islower():
			return False
		elif password.isupper():
			return False
		else:
			return True

class LoremIpsum(Nick, TextGenerator):
	'''Generate LoremIpsum text.'''
	start = ["lorem", "ipsum"]
	end = [".", "?", "!"]

	def __init__(self) -> None:
		self.sentence_length = 50
		self.word_randrange = (2, 8)


	def generate(self, Capitalize: bool = True) -> str:
		self.sentence = list()
		self.sentence += self.start
		self.previous_char = ""
		if self.sentence_length == 0:
			return ""
		elif self.word_randrange == (0, 0):
			return ""
		elif self.sentence_length == 1:
			return self.start[0]
		elif self.sentence_length == 2:
			return " ".join(self.start)


		for i in range(self.sentence_length-len(self.start)):
			super().set_length(random.randint(self.word_randrange[0], self.word_randrange[1]))
			self.sentence.append(self.__generate_nick())
		
		self.sentence = " ".join(self.sentence) + random.choice(self.end)

		if Capitalize is True:
			return self.sentence.capitalize()
		else:
			return self.sentence

	def __generate_nick(self, c: bool = False) -> str:
		return super().generate(c)

	def set_length(self, sentence_length: int):
		'''Set how many words will be generated.'''
		self.sentence_length = sentence_length

	def set_word_randrange(self, t: Tuple[int, int]):
		self.word_randrange = t[0], t[1]

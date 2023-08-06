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

import re
import os
import string
from typing import Any, Union, Tuple, List
from polyleven import levenshtein
try:
	# >=3.8
    from typing import Literal
except ImportError:
	# <=3.7
    from typing_extensions import Literal


def is_pangram(sentence: str, alphabet: str = string.ascii_lowercase) -> bool:
	'''Checks if inputed string is pangram
	(A pangram is a sentence using every letter of a given alphabet at least once.)
	- is_pangram('Watch "Jeopardy!", Alex Trebek\'s fun TV quiz game.') -> True
	- is_pangram('Hello beautiful world!') -> False
	'''
	#Checking if created set contains all characters from alphabet, and returning bool
	return set(alphabet.lower()) <= set(sentence.lower())

def is_heterogram(sentence: str) -> bool:
	'''Checks if inputed string is heterogram
	(A heterogram is a string in which no letter of the alphabet occurs more than once.)
	- is_heterogram("abcd") -> True
	- is_heterogram("abcdd") -> False
	'''
	return len(set(sentence.lower())) == len(sentence)

def is_anagram(first_word: str, second_word: str) -> bool:
	'''Checks if inputed string is an anagram
	(Anagram is a string that contain all letters from other string.)
	- is_anagram("Listen", "Silent") -> True
	- is_anagram("123", ("1234")) -> False
	'''
	return sorted(first_word.lower()) == sorted(second_word.lower())

def is_palindrome(obj: Union[str, int, List[Any], Tuple[Any]]) -> bool:
	'''Checks if inputed string is a palindrome
	(A palindrome is a word, number, phrase,
	or other sequence of characters which reads the same backward as forward,
	such as madam or racecar.)
		Takes Built-in Data Types (list, tuple, str, int)
	- is_palindrome("radar") -> True
	- is_palindrome("word") -> False
	'''
	try:
		return obj == obj[::-1]
	except TypeError:
		pass
	if type(obj) == int:
		return str(obj).replace(".", "") == str(obj)[::-1].replace(".", "")
	elif type(obj) == dict:
		return False # Dictionaries don't support duplicate keys, so it can't be palindrome.
	elif type(obj) == set and len(obj) == 1:
		return True
	elif type(obj) == set:
		return False # Sets don't support duplicate elements, so it can't be palindrome, unless there is only one element.

def is_tautogram(sentence: str) -> bool:
	'''Checks if inputed string is a tautogram
	(A tautogram is a text in which all words start with the same letter.)
	- is_tautogram("Crazy cat, cute, cuddly") -> True
	- is_tautogram("Crazy mouse, cute, cuddly") -> False
	'''
	return all(word[0].lower() == sentence[0].lower() for word in sentence.split())

class Spelling:
	'''Spell check words, get suggestions.
	Uses dictionaries (English, French...) saved in library.
	'''
	def __init__(self, language: Literal["en", "fr", "de", "ru"]) -> None:
		with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "languages", f"{language}.txt"), "r") as f:
			self.__correct_words = set(f.read().split("\n"))

	def is_correct(self, word: str,
			del_punctuation: bool = True,
			del_digits: bool = True) -> bool:
		'''Checks if given word is correct'''
		
		if del_punctuation:
			word = re.sub(r'[^\w\s]', '', word)
		if del_digits:
			word = re.sub(r'\d', '', word)

		w = word.split()
		for w in w:
			if w.lower() not in self.__correct_words:
				return False
		return True

	def get_suggestions(self, word: str, num: int = 10) -> List[str]:
		'''Get different correction suggestions on word'''
		suggestion = list()
		for correct_word in self.__correct_words:
			distance = levenshtein(word, correct_word)
			suggestion.append((correct_word, distance))

		suggestion.sort(key=lambda a: a[1]) # Sorting by levenshtein distance
		sorted_suggestion = list()
		# Replacing tuples with strings
		for word, d in suggestion:
			sorted_suggestion.append(word)
		
		# Returning only first x suggestions
		new_list = list()
		for i in range(num):
			new_list.append(sorted_suggestion.pop(0))

		return new_list

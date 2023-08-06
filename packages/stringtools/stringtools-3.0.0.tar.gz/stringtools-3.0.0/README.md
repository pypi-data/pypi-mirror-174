<p align="center">
<a href="https://github.com/Vazno/stringtools" target="_blank">
    <img src="https://raw.githubusercontent.com/Vazno/stringtools/main/readme-images/stringtools.svg" alt="Logo">
</p>

<p align="center">
    <em>stringtools provides string operations, such as analaysing, converting, generating, validating.</em>
</p>

<p align="center">
<a href="https://github.com/Vazno/stringtools/actions/workflows/pytester.yml" target="_blank">
    <img src="https://github.com/Vazno/stringtools/actions/workflows/pytester.yml/badge.svg?" alt="Tests">
</a>

<a href="https://pepy.tech/project/stringtools" target="_blank">
    <img src="https://pepy.tech/badge/stringtools" alt="Downloads">
</a>

<a href="https://lgtm.com/projects/g/Vazno/stringtools/context:python" target="_blank">
    <img src="https://img.shields.io/lgtm/grade/python/g/Vazno/stringtools.svg?logo=lgtm&logoWidth=18" alt="Quality">
</a>

<a href="https://pypi.org/project/stringtools" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/stringtools.svg?color=%2334D058" alt="Supported Python versions">
</a>

<p align="center">
<a href="https://github.com/Vazno/stringtools/actions/workflows/codeql-analysis.yml" target="_blank">
    <img src="https://github.com/Vazno/stringtools/actions/workflows/codeql-analysis.yml/badge.svg" alt="Analysis"</a>

---

**Source Code**: <a href="https://github.com/Vazno/stringtools" target="_blank">https://github.com/Vazno/stringtools</a>

**PyPI**: <a href="https://pypi.org/project/stringtools/" target="_blank">https://pypi.org/project/stringtools/</a>

---
stringtools has a lot of solutions specially built to be fast and stable ⚡.

The key features are:

* **Easy to use**: It has friendly and well-commented code.
* **Open source**: stringtools is completely free and [open source](https://opensource.org/about)
* **Stability**: Most of the code is covered with tests, so there is a less chance to catch a bug.

# Installation:
``pip install stringtools``


# User’s Guide:

## There are 5 categories:
### analaysers - Analyse string.
<p id="analysers"></p><table><tr><td><a href="#is_pangram">is_pangram</a>
</td><td><a href="#is_heterogram">is_heterogram</a>
</td><td><a href="#is_anagram">is_anagram</a>
</td><td><a href="#is_palindrome">is_palindrome</a>
</td></tr><tr><td><a href="#is_tautogram">is_tautogram</a>
</td><td><a href="Spelling">Spelling</a>
</td></tr></table>

### converters - Convert one string value to other string value.
<p id="converters"></p><table><tr><td><a href="#bricks">bricks</a>
</td><td><a href="#replaceall">replaceall</a>
</td><td><a href="#numerate_text">numerate_text</a>
</td><td><a href="#remove_trailing_whitespaces">remove_trailing_whitespaces</a>
</td></tr><tr><td><a href="#remove_leading_whitespaces">remove_leading_whitespaces</a>
</td><td><a href="#text_to_binary">text_to_binary</a>
</td><td><a href="#binary_to_text">binary_to_text</a>
</td><td><a href="#str_to_bool">str_to_bool</a>
</td></tr></table>

### general - General string operations.
<p id="general"></p><table><tr><td><a href="#Cases">Cases</a>
</td><td><a href="#Morse">Morse</a>
</td></tr></table>

### generators - Generate text inforamation.
<p id="generators"></p><table><tr><td><a href="#Nick">Nick</a>
</td><td><a href="#Password">Password</a>
</td><td><a href="#LoremIpsum">LoremIpsum</a>
</td></tr></table>

### validators - Validate ip, email addresses, e.t.c
<p id="validators"></p><table><tr><td><a href="#Validatorvalidate_semver">validate_semver</a>
</td><td><a href="#Validatorvalidate_email">validate_email</a>
</td><td><a href="#Validatorvalidate_ipv4">validate_ipv4</a>
</td><td><a href="#Validatorvalidate_ipv6">validate_ipv6</a>
</td></tr><tr><td><a href="#Validatorvalidate_url">validate_url</a>
</td></tr></table>


# Usage/Examples

## analaysers:
```python
from stringtools.analysers import *
```
#### ```is_pangram()```
#### <a href="#analysers">↑</a> Checks if inputed string is pangram (A pangram is a sentence using every letter of a given alphabet at least once.)
```python
is_pangram('Watch "Jeopardy!", Alex Trebek\'s fun TV quiz game.') 
# -> True
is_pangram('Hello beautiful world!') 
# -> False
```

#### ```is_heterogram()```
#### <a href="#analysers">↑</a> Checks if inputed string is heterogram (A heterogram is a string in which no letter of the alphabet occurs more than once.)
```python
is_heterogram("abcd")
# -> True
is_heterogram("abcdd")
# -> False
```

#### ```is_anagram()```
#### <a href="#analysers">↑</a> Checks if inputed string is an anagram (Anagram is a string that contain all letters from other string.)
```python
is_anagram("Tom Marvolo Riddle", "I Am Lord Voldemort")
# -> True
is_anagram("God", "Good")
# -> False
```

#### ```is_palindrome()```
#### <a href="#analysers">↑</a> Checks if inputed string is a palindrome (A palindrome is a word, number, phrase, or other sequence of characters which reads the same backward as forward, such as madam or racecar.)
```python
is_palindrome(["r","a","d","a","r"])
# -> True
is_palindrome(123)
# -> False
```

#### ```is_tautogram()```
#### <a href="#analysers">↑</a> Checks if inputed string is a tautogram (A tautogram is a text in which all words start with the same letter.)
```python
is_tautogram("Crazy cat, cute, cuddly")
# -> True
is_tautogram("Crazy mouse, cute, cuddly")
# -> False
```

#### ```Spelling```
#### <a href="#analysers">↑</a> Spell checker, which works by using levenshtein() function, can give correction suggestions, tell if a word is legit.
```python
s = Spelling("en")
s.is_correct("Hello")
# -> True
s.is_correct("eagoapesaf")
# -> False
s.get_suggestions("toxicit", 2)
# -> ['toxicity', 'solicit']
```


## converters:
```python
from stringtools.converters import *
```
#### ```bricks()```
#### <a href="#converters">↑</a> Returns bricked version of a string.
```python
bricks("Hello world!")
# -> "HeLlO WoRlD!
bricks("abcdef")
# -> "AbCdEf"
```

#### ```replaceall()```
#### <a href="#converters">↑</a> Replaces text from given sentence and dictionary.
dictionary should be formatted like this:
```python
{"old_string": "new_string"}
```
```python
replaceall("12345", {"1": "One ", "2": "Two ", "3": "Three "})
# -> "One Two Three 45"
replaceall("Hello world!", {"Hello": "Sup", "world": "earth"})
# -> "Sup earth!"
```

#### ```numerate_text()```
#### <a href="#converters">↑</a> Numerate each line of text.
```python
numerate_text("Hello world\nHow are you doing?")
# -> "1 Hello World\\n2 How are you doing?"
numerate_text("First line.\nThe second line\nThe third line")
# -> "1 First line.\n2 The second line\n3 The third line"
```

#### ```remove_trailing_whitespaces()```
#### <a href="#converters">↑</a> Remove all trailing whitespaces from sentence.

```python
remove_trailing_whitespaces("text   ")
# -> "text"
remove_trailing_whitespaces("Look at this. ")
# -> "Look at this."'''
```

#### ```remove_leading_whitespaces()```
#### <a href="#converters">↑</a> Remove all leading whitespaces from sentence.

```python
remove_leading_whitespaces("   text")
# -> "text"
remove_leading_whitespaces(" Look at this.")
# -> "Look at this."'''
```

#### ```text_to_binary()```
#### <a href="#converters">↑</a> Convert string to a binary (A binary number is a number expressed in the base-2 numeral system or binary numeral system, a method of mathematical expression which uses only two symbols: 0 and 1)

```python
text_to_binary("Hello")
# -> 0100100001100101011011000110110001101111
text_to_binary("A")
# -> 01000001
```

#### ```binary_to_text()```
#### <a href="#converters">↑</a> Convert binary to text (A binary number is a number expressed in the base-2 numeral system or binary numeral system, a method of mathematical expression which uses only two symbols: 0 and 1)

```python
binary_to_text("0100100001100101011011000110110001101111")
# -> "Hello"
binary_to_text("01000001")
# -> "A"'''
```

#### ```str_to_bool()```
#### <a href="#converters">↑</a> Converts a string representation of truth to bool
#####		False values are: "False", "f", "no", "n", "off", "0"
#####		True values are: "True", "t", "yes", "y", "on", "1"
```python
str_to_bool("True")
# -> True
str_to_bool("False")
# -> False
```


## general:
```python
from stringtools.general import *
```
#### ```Cases()```
#### <a href="#general">↑</a> Convert strings (and dictionary keys) between cases, and analyse.
##### Converting strings

```python
Cases.camelize("jack_in_the_box")
# -> "jackInTheBox"
Cases.decamelize("rubyTuesdays")
# -> "ruby_tuesdays"
Cases.pascalize("red_robin")
# -> "RedRobin"
Cases.kebabize("white_castle")
# -> "white-castle"
```

##### Converting dictionary keys

```python
array = [{"attrOne": "foo"}, {"attrOne": "bar"}]
Cases.decamelize(array)
# -> [{"attr_one": "foo"}, {"attr_one": "bar"}]

array = [{"attr_one": "foo"}, {"attr_one": "bar"}]
Cases.camelize(array)
# -> [{"attrOne": "foo"}, {"attrOne": "bar"}]

array = [{'attr_one': 'foo'}, {'attr_one': 'bar'}]
Cases.kebabize(array)
# -> [{'attr-one': 'foo'}, {'attr-one': 'bar'}]

array = [{"attr_one": "foo"}, {"attr_one": "bar"}]
Cases.pascalize(array)
# -> [{"AttrOne": "foo"}, {"AttrOne": "bar"}]
```

##### Checking character casing

```python
Cases.is_camelcase("illWearYourGranddadsClothes")
# -> True
Cases.is_pascalcase("ILookIncredible")
# -> True
Cases.is_snakecase("im_in_this_big_coat")
# -> True
Cases.is_kebabcase('from-that-shop')
# -> True
Cases.is_camelcase("from_that_shop")
# -> False
Cases.is_snakecase("downTheRoad")
# -> False
Cases.is_kebabcase('from_that_shop')
# -> False

# what about abbrevations, acronyms, and initialisms? No problem!
Cases.decamelize("APIResponse")
# -> "api_response"
```

#### ```Morse()```
#### <a href="#general">↑</a> Convert sentence to morse code, and vice versa.
```python
print(Morse.encode("HELLO, WORLD!"))
# -> ".... . .-.. .-.. --- --..-- / .-- --- .-. .-.. -.. -.-.--"
print(Morse.decode(".... . .-.. .-.. --- --..-- / .-- --- .-. .-.. -.. -.-.--"))
# -> "HELLO, WORLD!"
```


## generators:
```python
from stringtools.generators import *
```
#### ```Nick()```
#### <a href="#generators">↑</a> Generate nicknames by inputed vowels, consonants, and other sounds.
```python
n = Nick()
n.set_length(5)
for i in range(20):
    print(n.generate())
# -> 
# "Irrol"
# "Uppuq"
# "Aguir"
# "Moury"
# "Uwrax"
# "Ezeoa"
# "Agaum"
# "Egeti"
# "Efuyu"
# "Iruek"
# "Qawze"
# "Oguei"
# "Hochu"
# "Maqod"
# "Suyff"
# "Idoor"
# "Keigh"
# "Uredi"
# "Eceuy"
# "Elere"
```

#### ```Password()```
#### <a href="#generators">↑</a> Generate very strong passwords.
##### You can choose these options for password:
- English (abcd...)
- Numerals (1234...)
- Special Symbols ('`<*...)
- Own symbols (Any)
- Exclude similar characters (1, l, L, 0, o, O, etc.)
```python
p = Password()
p.set_length(8)
p.add_symbols()
p.add_digits()
p.add_ascii_letters()
p.generate()
# -> "C-3?r#$a"
p = Password()
p.set_length(16)
p.add_own("123")
# -> "3312311232131231"
print(Password.is_strong("123456789qwerty"))
# -> False
print(Password.is_strong("Aa0D#4v17@13.-0"))
# -> True
```

#### ```LoremIpsum()```
#### <a href="#generators">↑</a> Generate Lorem Ipsum text. (Lorem ipsum is a placeholder text commonly used to demonstrate the visual form of a document or a typeface without relying on meaningful content.)
```python
x = LoremIpsum()
x.set_length(5)
x.set_word_randrange((4, 10))
print(x.generate())
# -> "Lorem ipsum etnnimouft orknore zeoozeea."
print(x.generate())
# -> "Lorem ipsum eodyr gueipnaive pnaiz."
```


## validators:
```python
from stringtools.validators import *
```
#### ```Validator.validate_semver()```
#### <a href="#validators">↑</a> Validate if version name follows semantic versioning. For more information go to: https://semver.org/
```python
Validator.validate_semver("1.0.0")
# -> True
Validator.validate_semver("1.0.0.0")
# -> False
```

#### ```Validator.validate_email()```
#### <a href="#validators">↑</a> Validate an email address.
```python
Validator.validate_email("email@example.com")
# -> True
Validator.validate_email("email@example..com")
# -> False
```
#### ```Validator.validate_url()```
#### <a href="#validators">↑</a> Validate url address.
```python
Validator.validate_url("https://example.com/")
# -> True
Validator.validate_url("example.com")
# -> False
```

#### ```Validator.validate_ipv4()```
#### <a href="#validators">↑</a> Validate an ipv4 address.
```python
Validator.validate_ipv4("127.255.255.254")
# -> True
Validator.validate_ipv4("127.255.254")
# -> False
```

#### ```Validator.validate_ipv6()```
#### <a href="#validators">↑</a> Validate an ipv6 address.
```python
Validator.validate_ipv6("2345:0425:2CA1:0000:0000:0567:5673:23b5")
# -> True
Validator.validate_ipv6("0425:2CA1:0000:0000:0567:5673:23b5")
# -> False
```


# Authors

- [@Vazno](https://www.github.com/Vazno)

## License 🔑

[MIT](https://choosealicense.com/licenses/mit/) - Copyright (c) 2022 [Beksultan Artykbaev](https://github.com/Vazno)

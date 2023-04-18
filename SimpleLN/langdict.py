"""
    Created by Red-exe-Egineer/Wallee#8314
"""

import re

TITLE_STRING = re.compile(r'\[[a-zA-Z_-]+(\s+\[[a-zA-Z _-]+\])?\]\s*[a-zA-Z ]*')


class LangDict:
    """
        A class for storing language translations as dictionaries.

        The LangDict class reads a text file containing translations for multiple
        languages, and stores them as dictionaries. The text file should have the
        following format:

            [en]
            word1 = translation1
            word2 = translation2

        Each language code is enclosed in square brackets, and is followed by a list
        of translations for that language. If the language code is followed by one or
        more additional language codes, the translations for those languages will
        be inherited and merged into the current language dictionary. The inheritance
        is processed from left to right, with later languages overriding earlier ones.

            [en_US] en
            color = color

            [en_UK] en
            color = colour

        Example usage:
        >>> lang_dict = LangDict("translations.txt")
        >>> print(lang_dict.en["hello"])
        "Hello!"
        >>> print(lang_dict.es["hello"])
        "Hola!"

        Attributes:
            __init__(self, path: str): Initializes a new LangDict instance with
                translations from the specified text file.
            
            __str__(self): Returns a string representation of the LangDict instance,
                showing the language codes and the number of translations in each language.
            
            __contains__(self, language): Checks if the specified language code is
                present in the LangDict instance.
            
            codes(self): Returns a tuple of all the language codes present in the
                LangDict instance. Inherited codes are not included in the result.
    """

    def __init__(self, path: str):
        with open(path, "r") as file:
            lines = list(map(str.strip, file.read().split("\n")))

        current_lang = None
        inherit = {}

        for i, line in enumerate(lines, 1):
            if not line:
                continue

            if result := TITLE_STRING.search(line):
                current_lang = result.group().strip().split(" ")

                if len(current_lang) == 1:
                    current_lang, inherit = current_lang[0], {}
                else:
                    current_lang, inherit = current_lang[0], current_lang[1:]
                    inherit = [getattr(self, inherit).copy() for inherit in inherit]

                current_lang = current_lang[1:-1]

                assert getattr(self, current_lang, True), f'Line {i} in {path}:\n\t{current_lang} already created in file.'
                self.__setattr__(current_lang, {})

                for value in inherit:
                    getattr(self, current_lang).update(value)

            elif "=" in line:
                assert current_lang, f'Line {i} in {path}:\n\tLanguage not set before word definition.'
                name, value = line.split("=")
                getattr(self, current_lang)[name.strip()] = value.strip()

            else:
                raise ValueError(f'Invalid line format\n\tLine {i} in {path}: "{line}"')

    def __str__(self):
        return ", ".join([f'{code} ({len(words)})' for code, words in self.__dict__.items()])

    def __contains__(self, language):
        return hasattr(self, language)

    def codes(self):
        return tuple(sorted(set(self.__dict__) - {"__doc__", "__module__"}))

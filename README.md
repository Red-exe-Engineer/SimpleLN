# SimpleLN
A simple way to work with multi-lingual Python projects.

# Usage

### main.py
```python
from SimpleLN import LangDict

langs = LangDict("words.lang")

print(langs.en["hi"])  # "Hello"
print(langs.es["hi"])  # "Hola"
```

### words.lang
```
[en]
hi = Hello

[es]
hi = Hola
```

# Language inheritance
SimpleLN allows for one language to be based on another by adding the language name/code after the closing square bracket.

### main.py
```python
from SimpleLN import LangDict

langs = LangDict("words.lang")

print(langs.en_US["color"])  # "Color"
print(langs.en_UK["color"])  # "Colour"
```

### words.lang
```
[en]
hi = Hello

[en_US] en
color = Color

[en_UK] en
color = Colour
```

Note: a language can inherit from multiple languages (`[lang] lang1 lang2 lang3 ...`) and are loading in a left-to-right order.
This means that if lang1 has a `hi = hi` and lang2 has `hi = hey` doing `langs.lang["hi"]` will give "hey".

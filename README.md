# pyYandexTranslate
Library for Yandex Linguistics APIs for Python 3.3+

include:
* Yandex Translate API
* Yandex Dictionary API
* Yandex Predictor API

### Installation
`pip install pyYandexTranslate`

### Examples
```python
from pyYandexLinguistics import Translator, Dictionary, Predictor
import os

t = Translator(os.environ.get("KEY_FOR_TRANSLATOR_API"))
t.ok  # check api key is correct
# True
t.translate("Hello", 'es')
# {'lang': 'en-es', 'detected': {'lang': 'en'}, 'text': ['Hola']}

d = Dictionary(os.environ.get("KEY_FOR_DICTIONARY_API"))
d.ok
# True
d.lookup("Hello", 'en-es')
# {'def': [{'ts': '\u02c8he\u02c8l\u0259\u028a', 'tr': [{'pos': 'verb', 'text': 'saludar', 'mean': [{'text': 'greeting'}]}], 'pos': 'noun', 'text': 'hello'}]}

p = Predictor(os.environ.get("KEY_FOR_PREDICTOR_API"))
p.ok
# True
p.complete("en", "pyth", limit=5)
# {'pos': -4, 'text': ['python'], 'endOfWord': False}
```

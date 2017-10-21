from pyLinguist.mixins import YaTranslateException, YaBaseAPIHandler


class Dictionary(YaBaseAPIHandler):
    """
        Implements Yandex Dictionary API methods

        for more info look on https://tech.yandex.com/dictionary/
    """
    _base_url = r"https://dictionary.yandex.net/api/v{version}/" \
                r"dicservice{json}/"
    _endpoints = YaBaseAPIHandler._endpoints.copy()
    _endpoints.update({
        'lookup': "lookup"
    })

    # filters could be combined throw bitmap arithmetic
    NON_FILTERED = 0  # Remove all filters
    FAMILY = 1  # Apply the family search filter
    MORPHO = 4  # Enable searching by word form
    # Enable a filter that requires matching parts of speech for the search
    # word and translation:
    POS_FILTER = 8

    def __init__(self, api_key: str, xml: bool=False, version: str='1'):
        super(Dictionary, self).__init__(api_key, xml, version)
        self._url = self._base_url.format(version=self._v, json=self._json)

    def get_langs(self, **params) -> ...:
        """
            Wrapper for 'getLangs' API method.

            Use caching to store received info.
            https://tech.yandex.com/dictionary/doc/dg/reference/getLangs-docpage
        """
        return super(Dictionary, self)._get_langs(self._url, **params)

    def getLangs(self, **params) -> ...:
        return self.get_langs(**params)

    @property
    def ok(self) -> bool:
        """API key is correct"""
        return super(Dictionary, self)._ok(self._url)

    def lookup(self, text: str, lang: str, ui: str='en', flags: int=0,
               post: bool=False, **parameters) -> ...:
        """
            Wrapper for 'lookup' API method

            https://tech.yandex.com/dictionary/doc/dg/reference/lookup-docpage/

            Attributes:
            def - array of dictionary entries
            ts - a transcription of the search word
            tr - array of translations
            syn - array of synonyms
            mean - array of meanings
            ex - array of examples

            Subattributes:
            text - text of the entry, translation, or synonym (mandatory)
            pos - part of speech (may be omitted)
        """
        if lang not in self.get_langs():
            raise YaTranslateException(501)
        params = super(Dictionary, self)._form_params(
            text=text,
            lang=lang,
            ui=ui,
            flags=flags,
            **parameters
        )
        response = super(Dictionary, self).make_combined_request(
            "lookup", post, **params
        )
        if self._json:
            del response['head']  # depreciated attribute
        return response

    def definitions(self, text: str, lang: str, **params) -> ...:
        """
            Shortcut for lookup(...)['def']

            Return array of dictionary entries.
            A transcription of the search word may be provided in the 'ts' attribute.
        """
        if "callback" in params:
            raise ValueError("Wrong usage of callback")
        elif not self._json:
            return NotImplemented
        return self.lookup(text, lang, **params).get("def", None)


class Speller(YaBaseAPIHandler):
    """
        Implements Yandex Speller API methods

        for more info look on https://tech.yandex.ru/speller/
        no SOAP interface available
    """
    _base_url = r"http://speller.yandex.net/services/spellservice{json}/"
    _endpoints = {
        'text': "checkText",
        'texts': "checkTexts"
    }

    # options could be combined throw arithmetic (not bitmap!)
    IGNORE_UPPERCASE = 1  # (e.g. "DOTA")
    IGNORE_DIGITS = 2
    IGNORE_URLS = 4
    FIND_REPEAT_WORDS = 8  # (e.g. "What _is is_ going to be then?")
    IGNORE_LATIN = 16
    NO_SUGGEST = 32  # only check text without correction suggestions
    FLAG_LATIN = 128
    BY_WORDS = 256  # don't use context
    IGNORE_CAPITALIZATION = 512  # ignore wrong capitalization (e.g. "aLeX")
    IGNORE_ROMAN_NUMERALS = 2048

    # error codes
    ERROR_UNKNOWN_WORD = 1  # there is no such word in dictionary
    ERROR_REPEAT_WORD = 2
    ERROR_CAPITALIZATION = 3
    ERROR_TOO_MANY_ERRORS = 4

    def __init__(self, xml: bool=False, encoding: str='utf-8', **kwargs):
        super(Speller, self).__init__(kwargs.get('api_key', '_'), xml)
        if encoding.lower() not in self.encodings:
            raise ValueError("Wrong encoding: {}".format(encoding.lower()))
        self._ie = encoding.lower()
        self._url = self._base_url.format(json=self._json)

    def get_langs(self) -> set:
        """List of supported languages"""
        return {'ru', 'en', 'ua'}

    def getLangs(self) -> set:
        return self.get_langs()

    @property
    def encodings(self) -> set:
        """Collection of supported encodings"""
        return {"utf-8", "1251"}

    @property
    def ok(self) -> bool:
        """Successfully connect"""
        return super(Speller, self)._ok(None, self.check_text, "hello")

    def _check(self, endpoint: str, text: str or list, lang: list=["ru", "en"],
               options: int=0, fmt: str="plain", post: bool=False,
               **parameters) -> ...:
        """
            Wrapper for 'getText' and 'getTexts' API methods.

            https://tech.yandex.ru/speller/doc/dg/reference/checkText-docpage/
            https://tech.yandex.ru/speller/doc/dg/reference/checkTexts-docpage/

            Attributes:
            error – info about error (or errors, each object is separate error)
            word – original word
            s – hint (could be None, one or many)
            code – error code
            pos – position of incorrect word
            row – row of error
            col – number or column with error
            len – length of incorrect word
        """
        if endpoint not in self._endpoints:
            raise ValueError("wrong endpoint {}".format(endpoint))
        if post:
            return NotImplemented
        if list(filter((lambda l: l not in self.get_langs()), lang)):
            raise YaTranslateException(501)
        params = super(Speller, self)._form_params(
            text=text,
            lang=",".join(lang),
            options=options,
            format=fmt,
            ie=self._ie,
            **parameters
        )
        return super(Speller, self).make_combined_request(
            endpoint, post=False, **params
        )

    def check_text(self, text: str, lang: list=["ru", "en"], options: int=0,
                   fmt: str="plain", post: bool=False, **parameters) -> ...:
        """
            Wrapper for getText API method.
            https://tech.yandex.ru/speller/doc/dg/reference/checkText-docpage/
        """
        return self._check(
            endpoint="text",
            text=text,
            lang=lang,
            options=options,
            fmt=fmt,
            post=post,
            **parameters
        )

    def checkText(self, text: str, **params) -> ...:
        return self.check_text(text, **params)

    def check_texts(self, text: list, lang: list=["ru", "en"], options: int=0,
                    fmt: str="plain", post: bool=False, **parameters) -> ...:
        """
            Wrapper for getTexts API method.
            https://tech.yandex.ru/speller/doc/dg/reference/checkTexts-docpage/
        """
        return self._check(
            endpoint="texts",
            text=text,
            lang=lang,
            options=options,
            fmt=fmt,
            post=post,
            **parameters
        )

    def checkTexts(self, text: list, **params) -> ...:
        return self.check_texts(text, **params)

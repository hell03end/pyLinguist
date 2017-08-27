from . import YaTranslateException, _YaAPIHandler, logger


class Dictionary(_YaAPIHandler):
    """
        Implements Yandex Dictionary API methods

        for more info look on https://tech.yandex.com/dictionary/
        Underscoring is used for methods names instead of Camel Case
    """
    _base_url = r"https://dictionary.yandex.net/api/v{version}/" \
        r"dicservice{json}/"
    _endpoints = _YaAPIHandler._endpoints.copy()
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
        """
        :param api_key: :type str, personal API access key, given by Yandex
        :param xml: :type bool, specify returned data format
        :param version: :type str=1 – api version

        >>> Dictionary("123")._api_key == "123"  # test for parent method
        True
        >>> Dictionary("123").v == '1'
        True
        >>> Dictionary("123", version='1.5').v == '1.5'
        True
        >>> Dictionary("123")._url
        'https://dictionary.yandex.net/api/v1/dicservice.json/'
        """
        super(Dictionary, self).__init__(api_key, xml)
        self.v = version
        self._url = self._base_url.format(version=self.v, json=self._json)

    def get_langs(self, **params) -> ...:
        """
        Wrapper for getLangs API method. Use caching to store received info.
        https://tech.yandex.com/dictionary/doc/dg/reference/getLangs-docpage/

        :param params: supported additional params: callback, proxies
        :return: :type list, list of supported languages
        """
        return super(Dictionary, self)._get_langs(self._url, **params)

    @property
    def ok(self) -> bool:
        """
        To check that the API key is correct.

        :return: :type bool
        """
        return super(Dictionary, self)._ok(self._url)

    def lookup(self, text: str, lang: str, ui: str='en', flags: int=0,
               post: bool=False, **parameters) -> ...:
        """
        Wrapper for lookup API method.
        https://tech.yandex.com/dictionary/doc/dg/reference/lookup-docpage/

        Attributes:
        def â€” array of dictionary entries
        ts â€” a transcription of the search word
        tr â€” array of translations
        syn â€” array of synonyms
        mean â€” array of meanings
        ex â€” array of examples

        Subattributes:
        text â€” text of the entry, translation, or synonym (mandatory)
        pos â€” part of speech (may be omitted)

        :param text: :type str, the word or phrase to find in the dictionary
        :param lang: :type str, translation direction (set as a pair of language codes separated by a hyphen)
        :param ui: :type str='en', the language of the user's interface for displaying names of parts of speech in the dictionary entry
        :param flags: :type int=0, search options (bitmask of flags)
        :param post: :type bool=False, key for making POST request instead GET
        :param parameters: supported additional params: callback, proxies
        :return: :type dict or xml.etree.ElementTree.ElementTree or requests.Response
        :exception YaTranslateException, ConnectionError from requests.exceptions
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
        Shortcut for lookup(...)['def'].
        Return array of dictionary entries.
        A transcription of the search word may be provided in the 'ts' attribute.

        :param text: :type str, the word or phrase to find in the dictionary
        :param lang: :type str, translation direction (set as a pair of language codes separated by a hyphen)
        :param params: dict of additional params
        :return list, None or NotImplemented
        :exception YaTranslateException, ConnectionError from requests.exceptions, ValueError

        >>> Dictionary("123", xml=True).definitions("hello", "en-en")
        NotImplemented
        >>> Dictionary("123").definitions("hello", "en-en", callback=abs)
        Traceback (most recent call last):
            ...
        ValueError: definitions() Wrong usage of callback
        """
        if "callback" in params:
            raise ValueError("Wrong usage of callback")
        elif not self._json:
            return NotImplemented
        return self.lookup(text, lang, **params).get("def", None)


class Speller(_YaAPIHandler):
    """
        Implements Yandex Speller API methods

        for more info look on https://tech.yandex.ru/speller/
        Underscoring is used for methods names instead of Camel Case
        no SOAP interface available
    """
    _base_url = r"http://speller.yandex.net/services/spellservice{json}/"
    _endpoints = {
        'text': "checkText",
        'texts': "checkTexts"
    }
    _languages = {'ru', 'en', 'ua'}
    _encodings = {"utf-8", "1251"}

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
        """
        :param xml: :type bool, specify returned data format (json/xml)
        :param encoding: :type str='utf-8', possible variants: 'utf-8', '1251'

        >>> Speller()._api_key == '_'  # test for parent method
        True
        >>> Speller()._ie == "utf-8"
        True
        >>> Speller(encoding="1251")._ie == "1251"
        True
        >>> Speller(encoding="wubbalubbadubdub")
        Traceback (most recent call last):
            ...
        ValueError: Wrong encoding: wubbalubbadubdub
        """
        super(Speller, self).__init__(kwargs.get('api_key', '_'), xml)
        if encoding.lower() not in self._encodings:
            raise ValueError("Wrong encoding: {}".format(encoding.lower()))
        self._ie = encoding.lower()
        self._url = self._base_url.format(json=self._json)

    # @TODO: request to any of service apis
    @property
    def ok(self) -> bool:
        """
        No need to test api key.

        :return: :type bool
        """
        try:
            __ = self.check_text("hello")
        except BaseException as err:
            logger.warning(err)
            return False
        return True

    def _check(self, endpoint: str, text: str or list, lang: list=["ru", "en"],
               options: int=0, fmt: str="plain", post: bool=False,
               **parameters) -> ...:
        """
        Wrapper for getText and getTexts API methods.
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

        :param endpoint: :type str, method endpont
        :param text: :type str or list, the word or phrase to check
        :param lang: :type list, supported correction languages (possible values in Speller._languages)
        :param options: :type int, configurations for speller checker (flags)
        :param fmt: :type str, text format ('plain' or 'html')
        :param post: :type bool=False, key for making POST request instead GET
        :param parameters: supported additional params: callback, proxies
        :return: :type list or xml.etree.ElementTree.ElementTree or requests.Response
        :exception YaTranslateException, ValueError, ConnectionError from requests.exceptions
        """
        if endpoint not in self._endpoints:
            raise ValueError("wrong endpoint {}".format(endpoint))
        if post:
            return NotImplemented
        for lng in lang:
            if lng not in self._languages:
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
                   format: str="plain", post: bool=False,
                   **parameters) -> ...:
        """
        Wrapper for getText API method.
        https://tech.yandex.ru/speller/doc/dg/reference/checkText-docpage/

        :param text: :type str, the word or phrase to check
        :param lang: :type list=['ru', 'en'], supported correction languages (possible values in Speller._languages)
        :param options: :type int=0, configurations for speller checker (flags)
        :param format: :type str="plain", text format ('plain' or 'html')
        :param post: :type bool=False, key for making POST request instead GET
        :param parameters: supported additional params: callback, proxies
        :return: :type list or xml.etree.ElementTree.ElementTree or requests.Response
        :exception YaTranslateException, ValueError, ConnectionError from requests.exceptions
        """
        try:
            return self._check(
                endpoint="text",
                text=text,
                lang=lang,
                options=options,
                fmt=format,
                post=post,
                **parameters
            )
        except BaseException as err:
            raise err

    def check_texts(self, text: list, lang: list=["ru", "en"], options: int=0,
                    format: str="plain", post: bool=False,
                    **parameters) -> ...:
        """
        Wrapper for getTexts API method.
        https://tech.yandex.ru/speller/doc/dg/reference/checkTexts-docpage/

        :param text: :type list, the word or phrase to check
        :param lang: :type list=['ru', 'en'], supported correction languages (possible values in Speller._languages)
        :param options: :type int=0, configurations for speller checker (flags)
        :param format: :type str="plain", text format ('plain' or 'html')
        :param post: :type bool=False, key for making POST request instead GET
        :param parameters: supported additional params: callback, proxies
        :return: :type list or xml.etree.ElementTree.ElementTree or requests.Response
        :exception YaTranslateException, ValueError, ConnectionError from requests.exceptions
        """
        try:
            return self._check(
                endpoint="texts",
                text=text,
                lang=lang,
                options=options,
                fmt=format,
                post=post,
                **parameters
            )
        except BaseException as err:
            raise err

if __name__ == "__main__":
    import doctest
    doctest.testmod()

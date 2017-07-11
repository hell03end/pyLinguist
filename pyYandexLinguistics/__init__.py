# coding: utf-8
"""
    This module implements Yandex Translate and Dictionary APIs for Python 3.3+

    Powered by Yandex.Translate — http://translate.yandex.com/
    Powered by Yandex.Dictionary — https://tech.yandex.com/dictionary/
"""

import requests


class YaTranslateException(Exception):
    """
        Class for possible exceptions during Yandex API usage
    """
    error_codes = {
        400: "Wrong parameter was specified",
        401: "Invalid API key",
        402: "Blocked API key",
        403: "Exceeded the daily limit on the amount of requests",
        404: "Exceeded the daily limit on the amount of translated text",
        413: "Exceeded the maximum text size",
        422: "The text cannot be translated",
        501: "The specified translation direction is not supported",
        503: "Server not available",
    }

    def __init__(self, status_code: int, *args, **kwargs):
        """
        :param status_code: :type int, code, returned from request to API

        >>> YaTranslateException()
        Traceback (most recent call last):
            ...
        TypeError: __init__() missing 1 required positional argument: 'status_code'
        >>> YaTranslateException(400)
        YaTranslateException('Wrong parameter was specified', 400)
        >>> YaTranslateException(300)
        YaTranslateException('Unknown code', 300)
        >>> isinstance(YaTranslateException(400).error_codes, dict)
        True
        """
        message = self.error_codes.get(status_code, "Unknown code")
        super(YaTranslateException, self).__init__(message, status_code,
                                                   *args, **kwargs)


class _YaAPIHandler:
    """
        Generic class for Yandex APIs
    """
    _base_url = r""  # base api url for all requests
    _endpoints = {}

    def __init__(self, api_key: str, xml: bool=False, **kwargs):
        """
        :param api_key: :type str, personal API access key, given by Yandex
        :param xml: :type bool, specify returned data format

        >>> _YaAPIHandler()
        Traceback (most recent call last):
            ...
        TypeError: __init__() missing 1 required positional argument: 'api_key'
        >>> _YaAPIHandler('')
        Traceback (most recent call last):
            ...
        YaTranslateException: ('Invalid API key', 401)
        >>> _YaAPIHandler("123")._api_key == "123"
        True
        >>> _YaAPIHandler("123")._json == ".json"
        True
        >>> not _YaAPIHandler("123")._url
        True
        """
        if not api_key:
            raise YaTranslateException(401)
        self._api_key = api_key
        self._json = ".json" if not xml else ""
        self._url = self._base_url

    def _make_url(self, endpoint: str) -> str:
        """
        Creates full (base url + endpoint) url for API requests.

        :param endpoint: :type str, one of the keys from self._endpoints dict
        :return: :type str, created url for requests

        >>> not _YaAPIHandler("123")._make_url('')
        True
        """
        return self._url + self._endpoints.get(endpoint, '')

    def _form_params(self, callback=None, **kwargs) -> dict:
        """
        Returns dict of params for request, including API key and additional params.

        :param callback: name of callback function for JSONB response
        :param kwargs: :type dict, dict of named params
        :return: :type dict, formed params for future requests

        >>> _YaAPIHandler("123")._form_params()
        {'key': '123'}
        >>> 'ui' in _YaAPIHandler("123")._form_params(ui='en')
        True
        >>> 'callback' in _YaAPIHandler("123")._form_params("f")
        True
        >>> 'callback' not in _YaAPIHandler("123", xml=True)._form_params("f")
        True
        """
        params = {}
        for kwarg in kwargs:
            params[kwarg] = kwargs[kwarg]
        params['key'] = self._api_key
        if callback and self._json:  # for JSONB response
            params['callback'] = callback
        return params

    @staticmethod
    def _make_request(url: str, post: bool=False, **kwargs) -> dict:
        """
        Implements request to API with given params and return content in JSON.

        :param url: :type str, prepared url for request to API
        :param post: :type bool, key for making POST request instead GET
        :param kwargs: additional params for request, transmitted throw 'params' argument
        :return: :type dict, response content in JSON (response.json())
        :exception YaTranslateException, ConnectionError from requests.exceptions
        """
        if post:
            response = requests.post(url, params=kwargs)
        else:
            response = requests.get(url, params=kwargs)
        if not response.ok:
            raise YaTranslateException(response.status_code)
        return response.json()

    @property
    def ok(self) -> bool:
        """
        Implement it for testing api key is correct

        >>> _YaAPIHandler("123").ok
        True
        """
        try:
            # some simple request
            return True
        except:
            return False


class Translator(_YaAPIHandler):
    """
        Implements all Yandex Translator API methods

        for more info look on https://tech.yandex.com/translate/
        Underscoring is used for methods names instead of Camel Case
    """
    _base_url = r"https://translate.yandex.net/api/v{version}/tr{json}/"
    _endpoints = {
        'langs': "getLangs",
        'detect': "detect",
        'translate': "translate"
    }

    def __init__(self, api_key: str, xml: bool=False, **kwargs):
        """
        :param api_key: :type str, personal API access key, given by Yandex
        :param xml: :type bool, specify returned data format
        :param kwargs: supported additional params: version: int=1.5

        >>> Translator("123")._api_key == "123"  # test for parent method
        True
        >>> Translator("123").v == 1.5
        True
        >>> Translator("123", version=1).v == 1
        True
        >>> Translator("123")._url
        'https://translate.yandex.net/api/v1.5/tr.json/'
        """
        super(Translator, self).__init__(api_key, xml, **kwargs)
        self.v = kwargs.get("version", 1.5)
        self._url = self._base_url.format(version=self.v, json=self._json)

    def get_langs(self, lang: str='en', **kwargs) -> dict:
        """
        Wrapper for getLangs API method.
        https://tech.yandex.com/translate/doc/dg/reference/getLangs-docpage/

        :param lang: :type str='en', language names are output in the language corresponding to the code in this parameter
        :param kwargs: supported additional params: callback, proxies
        :return: :type dict
        """
        params = super(Translator, self)._form_params(
            callback=kwargs.get("callback", None), ui=lang, **kwargs
        )
        return super(Translator, self)._make_request(
            super(Translator, self)._make_url("langs"), post=False, **params)

    @property
    def directions(self, **kwargs) -> list:
        """
        Shortcut for get_langs(...)['dirs'].

        :return: :type list, list of supported directions of translation
        """
        return self.get_langs(**kwargs)['dirs']

    @property
    def languages(self, **kwargs) -> dict:
        """
        Shortcut for get_langs(...)['langs'].

        :return: :type dict, dict of supported languages
        """
        return self.get_langs(**kwargs)['langs']

    @property
    def ok(self) -> bool:
        """
        To check that the API key is correct.

        :return: :type bool
        """
        try:
            self.get_langs()
            return True
        except:
            return False

    def detect(self, text: str, hint: list=None, post: bool=False,
               **kwargs) -> str:
        """
        Wrapper for detect API method.
        https://tech.yandex.com/translate/doc/dg/reference/detect-docpage/

        :param text: :type str, text to detect the language for
        :param hint: :type list=None, list of the most likely languages (they will be given preference when detecting the text language)
        :param post: :type bool=False, key for making POST request instead GET
        :param kwargs: supported additional params: callback, proxies
        :return: :type str, code of detected language
        """
        if hint and not isinstance(hint, list):
            raise ValueError("'hint' should be type <class: list>")
        params = super(Translator, self)._form_params(
            callback=kwargs.get("callback", None), text=text, hint=hint,
            **kwargs
        )
        return super(Translator, self)._make_request(
            super(Translator, self)._make_url("detect"),
            post, **params)['lang']

    def translate(self, text: str or list, language: str,
                  formatting: str="plain", options: int=1, post: bool=False,
                  **kwargs) -> dict:
        """
        Wrapper for translate API method.
        https://tech.yandex.com/translate/doc/dg/reference/translate-docpage/

        :param text: :type str or list of str, text to translate
        :param language: :type str, the translation direction (or just the target language code)
        :param formatting: :type str='plain', text format ('plain' or 'html')
        :param options: :type int=1, the only option available at this time is whether the response should include the automatically detected language of the text being translated (options=1)
        :param post: :type bool=False, key for making POST request instead GET
        :param kwargs: supported additional params: callback, proxies
        :return: :type dict
        """
        params = super(Translator, self)._form_params(
            callback=kwargs.get("callback", None), text=text, lang=language,
            format=formatting, options=options, **kwargs
        )
        response = super(Translator, self)._make_request(
            super(Translator, self)._make_url("translate"), post, **params)
        del response["code"]  # this information is redundant
        return response


class Dictionary(_YaAPIHandler):
    """
        Implements all Yandex Dictionary API methods

        for more info look on https://tech.yandex.com/dictionary/
        Underscoring is used for methods names instead of Camel Case
    """
    _base_url = r"https://dictionary.yandex.net/api/v{version}/" \
                 r"dicservice{json}/"
    _endpoints = {
        'langs': "getLangs",
        'lookup': "lookup"
    }

    # filters could be combined throw bitmap arithmetic
    NON_FILTERED = 0  # Remove all filters
    FAMILY = 1  # Apply the family search filter
    MORPHO = 4  # Enable searching by word form
    # Enable a filter that requires matching parts of speech for the search
    # word and translation:
    POS_FILTER = 8

    def __init__(self, api_key: str, xml: bool=False, **kwargs):
        """
        :param api_key: :type str, personal API access key, given by Yandex
        :param xml: :type bool, specify returned data format
        :param kwargs: supported additional params: version: int=1

        >>> Dictionary("123")._api_key == "123"  # test for parent method
        True
        >>> Dictionary("123").v == 1
        True
        >>> Dictionary("123", version=1.5).v == 1.5
        True
        >>> Dictionary("123")._url
        'https://dictionary.yandex.net/api/v1/dicservice.json/'
        """
        super(Dictionary, self).__init__(api_key, xml, **kwargs)
        self.v = kwargs.get("version", 1)
        self._url = self._base_url.format(version=self.v, json=self._json)

    def get_langs(self, **kwargs) -> list:
        """
        Wrapper for getLangs API method.
        https://tech.yandex.com/dictionary/doc/dg/reference/getLangs-docpage/

        :param kwargs: supported additional params: callback, proxies
        :return: :type list, list of supported languages
        """
        params = super(Dictionary, self)._form_params(
            callback=kwargs.get("callback", None), **kwargs
        )
        return super(Dictionary, self)._make_request(
            super(Dictionary, self)._make_url("langs"), post=False, **params)

    @property
    def ok(self) -> bool:
        """
        To check that the API key is correct.

        :return: :type bool
        """
        try:
            self.get_langs()
        except:
            return False
        return True

    def lookup(self, text: str, lang: str, ui: str='en', flags: int=0,
               post: bool=False, **kwargs) -> dict:
        """
        Wrapper for lookup API method.
        https://tech.yandex.com/dictionary/doc/dg/reference/lookup-docpage/

        Attributes:
        def — array of dictionary entries
        ts — a transcription of the search word
        tr — array of translations
        syn — array of synonyms
        mean — array of meanings
        ex — array of examples

        Subattributes:
        text — text of the entry, translation, or synonym (mandatory)
        pos — part of speech (may be omitted)

        :param text: :type str, the word or phrase to find in the dictionary
        :param lang: :type str, translation direction (set as a pair of language codes separated by a hyphen)
        :param ui: :type str='en', the language of the user's interface for displaying names of parts of speech in the dictionary entry
        :param flags: :type int=0, search options (bitmask of flags)
        :param post: :type bool=False, key for making POST request instead GET
        :param kwargs: supported additional params: callback, proxies
        :return: :type dict
        """
        if lang not in self.get_langs():
            raise YaTranslateException(501)
        params = super(Dictionary, self)._form_params(
            callback=kwargs.get("callback", None), text=text, lang=lang, ui=ui,
            flags=flags, **kwargs
        )
        response = super(Dictionary, self)._make_request(
            super(Dictionary, self)._make_url("lookup"), post, **params)
        del response['head']  # depreciated
        return response

    def definitions(self, text: str, lang: str, **kwargs):
        """
        Shortcut for lookup(...)['def'].
        Return array of dictionary entries.
        A transcription of the search word may be provided in the 'ts' attribute.

        :param text: :type str, the word or phrase to find in the dictionary
        :param lang: :type str, translation direction (set as a pair of language codes separated by a hyphen)
        :param kwargs: dict of additional params
        """
        return self.lookup(text, lang, **kwargs).get("def", None)


class Predictor(_YaAPIHandler):
    """
        Implements all Yandex Predictor API methods

        for more info look on https://tech.yandex.ru/predictor/
        Underscoring is used for methods names instead of Camel Case
    """
    _base_url = r"https://predictor.yandex.net/api/v{version}/predict{json}/"
    _endpoints = {
        'langs': "getLangs",
        'complete': "complete"
    }

    def __init__(self, api_key: str, xml: bool=False, **kwargs):
        """
        :param api_key: :type str, personal API access key, given by Yandex
        :param xml: :type bool, specify returned data format
        :param kwargs: supported additional params: version: int=1

        >>> Predictor("123")._api_key == "123"  # test for parent method
        True
        >>> Predictor("123").v == 1
        True
        >>> Predictor("123", version=1.5).v == 1.5
        True
        >>> Predictor("123")._url
        'https://predictor.yandex.net/api/v1/predict.json/'
        """
        super(Predictor, self).__init__(api_key, xml, **kwargs)
        self.v = kwargs.get("version", 1)
        self._url = self._base_url.format(version=self.v, json=self._json)

    def get_langs(self, **kwargs) -> list:
        """
        Wrapper for getLangs API method.
        https://tech.yandex.ru/predictor/doc/dg/reference/getLangs-docpage/

        :param kwargs: supported additional params: callback, proxies
        :return: :type list, list of supported languages
        """
        params = super(Predictor, self)._form_params(
            callback=kwargs.get("callback", None), **kwargs
        )
        return super(Predictor, self)._make_request(
            super(Predictor, self)._make_url("langs"), post=False, **params)

    @property
    def ok(self) -> bool:
        """
        To check that the API key is correct.

        :return: :type bool
        """
        try:
            self.get_langs()
        except:
            return False
        return True

    def complete(self, lang: str, q: str, limit: int=1, post: bool=False,
                 **kwargs) -> dict:
        """
        Wrapper for complete API method.
        https://tech.yandex.ru/predictor/doc/dg/reference/complete-docpage/

        :param lang: :type str, text language
        :param q: :type str, text under user's pointer
        :param limit: :type int=1, max number of returned strings
        :param post: :type bool=False, key for making POST request instead GET
        :param kwargs: supported additional params: callback, proxies
        :return: :type dict
        """
        if lang not in self.get_langs():
            raise YaTranslateException(501)
        params = super(Predictor, self)._form_params(
            callback=kwargs.get("callback", None), lang=lang, q=q,
            limit=limit, **kwargs
        )
        return super(Predictor, self)._make_request(
            super(Predictor, self)._make_url("complete"), post, **params)


__all__ = ["Dictionary", "Translator", "YaTranslateException", "Predictor"]

if __name__ == "__main__":
    import doctest
    doctest.testmod()

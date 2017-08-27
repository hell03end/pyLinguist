from . import _YaAPIHandler


class Translator(_YaAPIHandler):
    """
        Implements all Yandex Translator API methods

        for more info look on https://tech.yandex.com/translate/
        Underscoring is used for methods names instead of Camel Case
    """
    _base_url = r"https://translate.yandex.net/api/v{version}/tr{json}/"
    _endpoints = _YaAPIHandler._endpoints.copy()
    _endpoints.update({
        'detect': "detect",
        'translate': "translate"
    })

    def __init__(self, api_key: str, xml: bool=False, version: str='1.5'):
        """
        :param api_key: :type str, personal API access key, given by Yandex
        :param xml: :type bool, specify returned data format
        :param kwargs: :type str='1.5' – api version

        >>> Translator("123")._api_key == "123"  # test for parent method
        True
        >>> Translator("123").v == '1.5'
        True
        >>> Translator("123", version='1').v == '1'
        True
        >>> Translator("123")._url
        'https://translate.yandex.net/api/v1.5/tr.json/'
        """
        super(Translator, self).__init__(api_key, xml)
        self.v = version
        self._url = self._base_url.format(version=self.v, json=self._json)

    def get_langs(self, lang: str='en', **params) -> ...:
        """
        Wrapper for getLangs API method. Use caching to store received info.
        https://tech.yandex.com/translate/doc/dg/reference/getLangs-docpage/

        :param lang: :type str='en', language names are output in the language corresponding to the code in this parameter
        :param params: supported additional params: callback, proxies, update
        :return: :type dict or list or ElementTree or requests.Response
        """
        return super(Translator, self)._get_langs(self._url, ui=lang, **params)

    @property
    def directions(self) -> list or None:
        """
        Shortcut for get_langs(...)['dirs'].

        :return: :type list or NotImplemented, list of supported directions of translation
        """
        if not self._json:
            return self.get_langs()
        return self.get_langs().get('dirs', None)

    @property
    def languages(self) -> list or None or NotImplemented:
        """
        Shortcut for get_langs(...)['langs'].

        :return: :type dict or None or NotImplemented, dict of supported languages
        """
        if not self._json:
            return NotImplemented
        return self.get_langs().get('langs', None)

    @property
    def ok(self) -> bool:
        """
        To check that the API key is correct.

        :return: :type bool
        """
        return super(Translator, self)._ok(self._url)

    def detect(self, text: str, hint: list=None, post: bool=False,
               **parameters) -> ...:
        """
        Wrapper for detect API method.
        https://tech.yandex.com/translate/doc/dg/reference/detect-docpage/

        :param text: :type str, text to detect the language for
        :param hint: :type list=None, list of the most likely languages (they will be given preference when detecting the text language)
        :param post: :type bool=False, key for making POST request instead GET
        :param parameters: supported additional params: callback, proxies
        :return: :type str or ElementTree or requests.Response
        :exception ValueError
        """
        if hint and not isinstance(hint, list):
            raise ValueError("'hint' should be type <class: list>")
        params = super(Translator, self)._form_params(
            text=text,
            hint=hint,
            **parameters
        )
        response = super(Translator, self).make_combined_request(
            "detect", post, **params
        )
        if self._json:
            return response['lang']
        return response

    def translate(self, text: str or list, language: str,
                  formatting: str="plain", options: int=1, post: bool=False,
                  **parameters) -> ...:
        """
        Wrapper for translate API method.
        https://tech.yandex.com/translate/doc/dg/reference/translate-docpage/

        :param text: :type str or list of str, text to translate
        :param language: :type str, the translation direction (or just the target language code)
        :param formatting: :type str='plain', text format ('plain' or 'html')
        :param options: :type int=1, the only option available at this time is whether the response should include the automatically detected language of the text being translated (options=1)
        :param post: :type bool=False, key for making POST request instead GET
        :param parameters: supported additional params: callback, proxies
        :return: :type dict or xml.etree.ElementTree.ElementTree
        """
        params = super(Translator, self)._form_params(
            text=text,
            lang=language,
            format=formatting,
            options=options,
            **parameters
        )
        response = super(Translator, self).make_combined_request(
            "translate", post, **params
        )
        if self._json:
            del response['code']  # this information is redundant
        return response


if __name__ == "__main__":
    import doctest
    doctest.testmod()

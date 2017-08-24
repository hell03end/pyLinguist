try:
    from . import YaTranslateException, _YaAPIHandler, logger
except ImportError as err:
    from pyYandexLinguistics import YaTranslateException, _YaAPIHandler, logger
    logger.debug(err)


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

    # @TODO: caching
    def get_langs(self, lang: str='en', **params) -> dict:
        """
        Wrapper for getLangs API method. Use caching to store received info.
        https://tech.yandex.com/translate/doc/dg/reference/getLangs-docpage/

        :param lang: :type str='en', language names are output in the language corresponding to the code in this parameter
        :param params: supported additional params: callback, proxies, update
        :return: :type dict
        """
        return super(Translator, self)._get_langs(self._url, ui=lang, **params)

    @property
    def directions(self) -> list:
        """
        Shortcut for get_langs(...)['dirs'].

        :return: :type list, list of supported directions of translation
        """
        return self.get_langs()['dirs']

    @property
    def languages(self) -> dict:
        """
        Shortcut for get_langs(...)['langs'].

        :return: :type dict, dict of supported languages
        """
        return self.get_langs()['langs']

    @property
    def ok(self) -> bool:
        """
        To check that the API key is correct.

        :return: :type bool
        """
        try:
            __ = self.get_langs(update=True)
        except BaseException as err:
            logger.warning(err)
            return False
        return True

    def detect(self, text: str, hint: list=None, post: bool=False,
               **parameters) -> str:
        """
        Wrapper for detect API method.
        https://tech.yandex.com/translate/doc/dg/reference/detect-docpage/

        :param text: :type str, text to detect the language for
        :param hint: :type list=None, list of the most likely languages (they will be given preference when detecting the text language)
        :param post: :type bool=False, key for making POST request instead GET
        :param parameters: supported additional params: callback, proxies
        :return: :type str, code of detected language
        """
        if hint and not isinstance(hint, list):
            raise ValueError("'hint' should be type <class: list>")
        params = super(Translator, self)._form_params(
            text=text,
            hint=hint,
            **parameters
        )
        return super(Translator, self)._make_request(
            super(Translator, self)._make_url("detect"),
            post,
            **params
        )['lang']

    def translate(self, text: str or list, language: str,
                  formatting: str="plain", options: int=1, post: bool=False,
                  **parameters) -> dict:
        """
        Wrapper for translate API method.
        https://tech.yandex.com/translate/doc/dg/reference/translate-docpage/

        :param text: :type str or list of str, text to translate
        :param language: :type str, the translation direction (or just the target language code)
        :param formatting: :type str='plain', text format ('plain' or 'html')
        :param options: :type int=1, the only option available at this time is whether the response should include the automatically detected language of the text being translated (options=1)
        :param post: :type bool=False, key for making POST request instead GET
        :param parameters: supported additional params: callback, proxies
        :return: :type dict
        """
        params = super(Translator, self)._form_params(
            text=text,
            lang=language,
            format=formatting,
            options=options,
            **parameters
        )
        response = super(Translator, self)._make_request(
            super(Translator, self)._make_url("translate"),
            post,
            **params
        )
        del response["code"]  # this information is redundant
        return response


if __name__ == "__main__":
    import doctest
    doctest.testmod()

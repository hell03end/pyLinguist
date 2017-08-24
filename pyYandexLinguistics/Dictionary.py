try:
    from . import YaTranslateException, _YaAPIHandler, logger
except ImportError as err:
    from pyYandexLinguistics import YaTranslateException, _YaAPIHandler, logger
    logger.debug(err)


class Dictionary(_YaAPIHandler):
    """
        Implements all Yandex Dictionary API methods

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

    def get_langs(self, **params) -> list:
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
        try:
            __ = self.get_langs(update=True)
        except BaseException as err:
            logger.warning(err)
            return False
        return True

    def lookup(self, text: str, lang: str, ui: str='en', flags: int=0,
               post: bool=False, **parameters) -> dict:
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
        :return: :type dict
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
        response = super(Dictionary, self)._make_request(
            super(Dictionary, self)._make_url("lookup"),
            post,
            **params
        )
        del response['head']  # depreciated
        return response

    # @TODO: add returned type annotation
    def definitions(self, text: str, lang: str, **params) -> list or None:
        """
        Shortcut for lookup(...)['def'].
        Return array of dictionary entries.
        A transcription of the search word may be provided in the 'ts' attribute.

        :param text: :type str, the word or phrase to find in the dictionary
        :param lang: :type str, translation direction (set as a pair of language codes separated by a hyphen)
        :param params: dict of additional params
        """
        return self.lookup(text, lang, **params).get("def", None)


if __name__ == "__main__":
    import doctest
    doctest.testmod()

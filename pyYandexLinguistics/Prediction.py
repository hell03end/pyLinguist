from . import YaTranslateException, _YaAPIHandler


class Predictor(_YaAPIHandler):
    """
        Implements all Yandex Predictor API methods

        for more info look on https://tech.yandex.ru/predictor/
        Underscoring is used for methods names instead of Camel Case
    """
    _base_url = r"https://predictor.yandex.net/api/v{version}/predict{json}/"
    _endpoints = _YaAPIHandler._endpoints.copy()
    _endpoints.update({
        'complete': "complete"
    })

    def __init__(self, api_key: str, xml: bool=False, version: str='1'):
        """
        :param api_key: :type str, personal API access key, given by Yandex
        :param xml: :type bool, specify returned data format
        :param version: :type str='1' – api version

        >>> Predictor("123")._api_key == "123"  # test for parent method
        True
        >>> Predictor("123").v == '1'
        True
        >>> Predictor("123", version='1.5').v == '1.5'
        True
        >>> Predictor("123")._url
        'https://predictor.yandex.net/api/v1/predict.json/'
        """
        super(Predictor, self).__init__(api_key, xml)
        self.v = version
        self._url = self._base_url.format(version=self.v, json=self._json)

    def get_langs(self, **params) -> list:
        """
        Wrapper for getLangs API method. Use caching to store received info.
        https://tech.yandex.ru/predictor/doc/dg/reference/getLangs-docpage/

        :param update: :type bool=False, update caching values
        :param params: supported additional params: callback, proxies
        :return: :type list, list of supported languages
        """
        return super(Predictor, self)._get_langs(self._url, **params)

    @property
    def ok(self) -> bool:
        """
        To check that the API key is correct.

        :return: :type bool
        """
        return super(Predictor, self)._ok(self._url)

    def complete(self, lang: str, q: str, limit: int=1, post: bool=False,
                 **parameters) -> dict:
        """
        Wrapper for complete API method.
        https://tech.yandex.ru/predictor/doc/dg/reference/complete-docpage/

        :param lang: :type str, text language
        :param q: :type str, text under user's pointer
        :param limit: :type int=1, max number of returned strings
        :param post: :type bool=False, key for making POST request instead GET
        :param parameters: supported additional params: callback, proxies
        :return: :type dict
        """
        if lang not in self.get_langs():
            raise YaTranslateException(501)
        params = super(Predictor, self)._form_params(
            lang=lang,
            q=q,
            limit=limit,
            **parameters
        )
        return super(Predictor, self)._make_request(
            super(Predictor, self)._make_url("complete"),
            post,
            **params
        )


if __name__ == "__main__":
    import doctest
    doctest.testmod()

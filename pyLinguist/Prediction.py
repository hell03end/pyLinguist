from . import YaTranslateException, YaBaseAPIHandler


class Predictor(YaBaseAPIHandler):
    """
        Implements all Yandex Predictor API methods

        for more info look on https://tech.yandex.ru/predictor/
    """
    _base_url = r"https://predictor.yandex.net/api/v{version}/predict{json}/"
    _endpoints = YaBaseAPIHandler._endpoints.copy()
    _endpoints.update({
        'complete': "complete"
    })

    def __init__(self, api_key: str, xml: bool=False, version: str='1'):
        super(Predictor, self).__init__(api_key, xml, version)
        self._url = self._base_url.format(version=self._v, json=self._json)

    def get_langs(self, **params) -> ...:
        """
            Wrapper for getLangs API method.
            Use caching to store received info.
            https://tech.yandex.ru/predictor/doc/dg/reference/getLangs-docpage/
        """
        return super(Predictor, self)._get_langs(self._url, **params)

    def getLangs(self, **params) -> ...:
        return self.get_langs(**params)

    @property
    def ok(self) -> bool:
        """API key is correct"""
        return super(Predictor, self)._ok(self._url)

    def complete(self, lang: str, q: str, limit: int=1, post: bool=False,
                 **parameters) -> ...:
        """
            Wrapper for 'complete' API method.

            https://tech.yandex.ru/predictor/doc/dg/reference/complete-docpage/
        """
        if lang not in self.get_langs():
            raise YaTranslateException(501)
        params = super(Predictor, self)._form_params(
            lang=lang,
            q=q,
            limit=limit,
            **parameters
        )
        return super(Predictor, self).make_combined_request(
            "complete", post, **params
        )

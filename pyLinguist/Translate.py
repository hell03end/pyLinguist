from . import _YaBaseAPIHandler


class Translator(_YaBaseAPIHandler):
    """
        Implements all Yandex Translator API methods

        for more info look on https://tech.yandex.com/translate/
    """
    _base_url = r"https://translate.yandex.net/api/v{version}/tr{json}/"
    _endpoints = _YaBaseAPIHandler._endpoints.copy()
    _endpoints.update({
        'detect': "detect",
        'translate': "translate"
    })

    def __init__(self, api_key: str, xml: bool=False, version: str='1.5'):
        super(Translator, self).__init__(api_key, xml, version)
        self._url = self._base_url.format(version=self._v, json=self._json)

    def get_langs(self, lang: str='en', **params) -> ...:
        """
            Wrapper for getLangs API method.

            Use caching to store received info.
            https://tech.yandex.com/translate/doc/dg/reference/getLangs-docpage
        """
        return super(Translator, self)._get_langs(self._url, ui=lang, **params)

    def getLangs(self, lang: str='en', **params) -> ...:
        return self.get_langs(lang, **params)

    @property
    def directions(self) -> list or None:
        """Shortcut for get_langs(...)['dirs']"""
        if not self._json:
            return self.get_langs()
        return self.get_langs().get('dirs', None)

    @property
    def languages(self) -> list or None or NotImplemented:
        """Shortcut for get_langs(...)['langs']"""
        if not self._json:
            return NotImplemented
        return self.get_langs().get('langs', None)

    @property
    def ok(self) -> bool:
        """API key is correct"""
        return super(Translator, self)._ok(self._url)

    def detect(self, text: str, hint: list=None, post: bool=False,
               **parameters) -> ...:
        """
            Wrapper for detect API method.

            https://tech.yandex.com/translate/doc/dg/reference/detect-docpage/
        """
        if hint and not isinstance(hint, list):
            raise ValueError("'hint' should be type {}".format(type(list)))
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

           https://tech.yandex.com/translate/doc/dg/reference/translate-docpage
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

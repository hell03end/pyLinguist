import re

from . import YaBaseAPIHandler


class Translator(YaBaseAPIHandler):
    """
        Implements all Yandex Translator API methods

        for more info look on https://tech.yandex.com/translate/
    """
    _base_url = r"https://translate.yandex.net/api/v{version}/tr{json}/"
    _endpoints = YaBaseAPIHandler._endpoints.copy()
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

    # @TODO: 2..10Kb for GET
    def _translate_long_get(self, text: str) -> ...:
        return NotImplemented

    # @TODO: 10K symbols for POST
    def _translate_long_post(self, text: str) -> ...:
        return NotImplemented

    # @TODO: add semantic separation
    @staticmethod
    def _separate_text(text: str, limit: int) -> list:
        size = len(text)
        parts_count = int((size + limit - 1) // limit)
        return [text[part:part + limit] for part in range(0, size, limit)]

    # @TODO: add list separation by contained text
    @staticmethod
    def _separate_texts(texts: list, limit: int) -> list:
        separated_list = [[]]
        partion_size = 0
        idx = 0
        for text in texts:
            if len(text) <= limit - partion_size:
                separated_list[idx].append(text)
                continue
            text_parts = Translator._separate_text(text, limit - partion_size)
            separated_list[idx].append((text_parts[0]))
            separated_list.append([])
            idx += 1
            separated_list[idx].append(("".join(text_parts[1:])))
            separated_list.append([])
            idx += 1
        return NotImplemented

    # @FIXME: some cases of parsing are incorrect
    @staticmethod
    def _str2list(text: str) -> str:
        if not isinstance(text, str):
            raise ValueError("Wrong type {}".format(type(text)))
        if "\\" in text:
            return re.split(r"\', \'", text.strip(r"[]").strip("\'"))
        return re.split("\', \'", text.strip(r"[]").strip("\'"))

    def translate(self, text: str or list, language: str,
                  formatting: str="plain", options: int=1, post: bool=False,
                  **parameters) -> ...:
        """
            Wrapper for translate API method.

           https://tech.yandex.com/translate/doc/dg/reference/translate-docpage
        """
        params = super(Translator, self)._form_params(
            text=text,
            list_exceptions={"text"},
            lang=language,
            format=formatting,
            options=options,
            ** parameters
        )
        # assume that unicode character is 2 bytes long and browser can handle
        # long GET requests (up to approximately 9Kb)
        if not post and isinstance(text, str) and len(text) >= (9 * 1024) / 2:
            self._logger.warning("Long text processing still not implemented!")
            ...
        elif post and isinstance(text, str) and len(text) >= 10000:
            self._logger.warning("Long text processing still not implemented!")
            ...
        response = super(Translator, self).make_combined_request(
            "translate", post, **params
        )
        if self._json:
            del response['code']  # this information is redundant
            if isinstance(text, list) and len(response['text']) == 1:
                self._logger.warning("List parsing still not implemented!")
                # response['text'] = self._str2list(response['text'][0])
        return response

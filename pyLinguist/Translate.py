import logging
import re

from pyLinguist.utils.base import YaBaseAPIHandler
from pyLinguist.utils.log import log


class Translator(YaBaseAPIHandler):
    """
        Implements all Yandex Translator API methods

        for more info look on https://tech.yandex.com/translate/
    """
    _base_url = r"https://translate.yandex.net/api/v{}/tr.json/"
    _endpoints = YaBaseAPIHandler._endpoints.copy()
    _endpoints.update({
        'detect': "detect",
        'translate': "translate"
    })

    def __init__(self, api_key: str, version: str='1.5', **kwargs):
        super(Translator, self).__init__(api_key, version, **kwargs)
        self._url = self._base_url.format(self._v)

    @log()
    def get_langs(self, lang: str='en') -> dict:
        """
            Wrapper for getLangs API method.

            Use caching to store received info.
            https://tech.yandex.com/translate/doc/dg/reference/getLangs-docpage
        """
        return super(Translator, self)._get_langs(self._url, ui=lang)

    def getLangs(self, lang: str='en') -> dict:
        return self.get_langs(lang)

    @property
    def directions(self) -> list:
        """ Shortcut for get_langs(...)['dirs'] """
        return self.get_langs().get('dirs', [])

    @property
    def languages(self) -> dict:
        """ Shortcut for get_langs(...)['langs'] """
        return self.get_langs().get('langs', [])

    @property
    def ok(self) -> bool:
        return super(Translator, self)._ok(self._url)

    @log()
    def detect(self,
               text: str,
               hint: list=None,
               post: bool=False,
               **params) -> str:
        """
            Wrapper for detect API method.

            https://tech.yandex.com/translate/doc/dg/reference/detect-docpage/
        """
        if hint and not isinstance(hint, (list, tuple)):
            raise ValueError(
                "'hint' should be iterable, got {}".format(type(hint))
            )

        params = super(Translator, self)._form_params(
            text=text,
            hint=hint,
            **params
        )
        response = super(Translator, self).make_request(
            Translator._make_url(self._url, "detect"), post, **params
        )
        return response['lang']

    # # @TODO: 2..10Kb for GET
    # def _translate_long_get(self, text: str) -> ...:
    #     return NotImplemented

    # # @TODO: 10K symbols for POST
    # def _translate_long_post(self, text: str) -> ...:
    #     return NotImplemented

    # # @TODO: add semantic separation
    # @staticmethod
    # def _separate_text(text: str, limit: int) -> list:
    #     size = len(text)
    #     parts_count = int((size + limit - 1) // limit)
    #     return [text[part:part + limit] for part in range(0, size, limit)]

    # # @TODO: add list separation by contained text
    # @staticmethod
    # def _separate_texts(texts: list, limit: int) -> list:
    #     separated_list = [[]]
    #     partion_size = 0
    #     idx = 0
    #     for text in texts:
    #         if len(text) <= limit - partion_size:
    #             separated_list[idx].append(text)
    #             continue
    #         text_parts = Translator._separate_text(text, limit - partion_size)
    #         separated_list[idx].append((text_parts[0]))
    #         separated_list.append([])
    #         idx += 1
    #         separated_list[idx].append(("".join(text_parts[1:])))
    #         separated_list.append([])
    #         idx += 1
    #     return NotImplemented

    # @FIXME: some cases of parsing are incorrect
    @staticmethod
    def _str2list(text: str) -> str:
        pattern = r"\', \'" if "\\" in text else "\', \'"
        return re.split(pattern, text.strip(r"[]").strip("\'"))

    @log()
    def translate(self,
                  text: str or list,
                  language: str,
                  formatting: str="plain",
                  options: int=1,
                  post: bool=False,
                  **params) -> dict:
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
            **params
        )
        # # assume that unicode character is 2 bytes long and browser can handle
        # # long GET requests (up to approximately 9Kb)
        # if not post and isinstance(text, str) and len(text) >= (9 * 1024) / 2:
        #     logging.warning("Long text processing still not implemented!")
        #     ...
        # elif post and isinstance(text, str) and len(text) >= 10000:
        #     logging.warning("Long text processing still not implemented!")
        #     ...
        response = super(Translator, self).make_request(
            Translator._make_url(self._url, "translate"), post, **params
        )

        del response['code']  # this information is redundant
        if isinstance(text, list) and len(response['text']) == 1:
            logging.warning("List parsing still not implemented well!")
            response['text'] = self._str2list(response['text'][0])
        return response

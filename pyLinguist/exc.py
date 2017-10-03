from .utils import ERROR_CODES


class YaTranslateException(Exception):
    """ Yandex API exceptions """
    error_codes = ERROR_CODES

    def __init__(self, status_code: int, *args, **kwargs):
        if not isinstance(status_code, int):
            raise ValueError("int required, got {}".format(type(status_code)))
        message = self.error_codes.get(
            status_code, "Unknown code {}".format(status_code)
        )
        super(YaTranslateException, self).__init__(
            message, status_code, *args, **kwargs
        )

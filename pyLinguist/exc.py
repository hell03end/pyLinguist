ERROR_CODES = {
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


class YaTranslateException(Exception):
    """
        Yandex API exceptions
    """
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

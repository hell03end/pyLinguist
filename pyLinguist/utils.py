LEVELS = {
    "NOTSET": 0,
    "DEBUG": 10,
    "INFO": 20,
    "WARN": 30,
    "WARNING": 30,
    "ERROR": 40,
    "FATAL": 50,
    "CRITICAL": 50
}

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


def Logger(name: str, level: int=LEVELS["DEBUG"], **kwargs) -> ...:
    import logging
    logging.basicConfig(
        format=kwargs.get(
            "format",
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        ),
        level=level
    )
    return logging.getLogger(name)

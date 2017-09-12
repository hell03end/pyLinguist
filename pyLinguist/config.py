LEVELS = {
    "DEBUG": 10,
    "INFO": 20,
    "WARNING": 30,
    "ERROR": 40,
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

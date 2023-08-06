import logging

import smartparams


class Log:
    init = logging.getLogger(f'{smartparams.__name__}.init')
    merge = logging.getLogger(f'{smartparams.__name__}.merge')
    register = logging.getLogger(f'{smartparams.__name__}.register')
    io = logging.getLogger(f'{smartparams.__name__}.io')
    import_ = logging.getLogger(f'{smartparams.__name__}.import')

    @staticmethod
    def setup() -> logging.Logger:
        fmt = "[%(asctime)s]\t%(threadName)10s\t%(name)-20s\t%(levelname)10s\t%(message)s"
        formatter = logging.Formatter(fmt)
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger = logging.getLogger(smartparams.__name__)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        return logger

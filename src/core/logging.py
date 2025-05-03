import logging
import logging.config


LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        },
    },
    'handlers': {
        'default': {
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        },
        'file_handler': {
            'formatter': 'standard',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'app.log',
            'maxBytes': 1024 * 1024 * 1,
        },
    },
    'root': {
        'level': 'INFO',
        'handlers': ['default', 'file_handler'],
    },
    'loggers': {
        'uvicorn': {
            'handlers': ['default', 'file_handler'],
            'level': 'TRACE',
            'propagate': False
        },
    }
}


def setup_logging():
    logging.config.dictConfig(LOGGING_CONFIG)

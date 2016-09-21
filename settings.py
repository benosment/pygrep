LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,

    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] [%(funcName)s:%(lineno)d] %(message)s',
            'datefmt': '%m/%d/%Y %I:%M:%S %p',
        },
    },

    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'log.txt',
            'formatter': 'standard'
        },
    },

    'loggers': {
        '': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
        }
    }
}

ignore_list = ['.CCACHE',
               'venv',
               '__pycache__',
               '.git',
               '.idea',
               ]

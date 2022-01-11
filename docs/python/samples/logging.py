# https://docs.djangoproject.com/en/3.2/topics/logging/#django-security
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "console": {
            "format": "%(asctime)s %(levelname)s [%(name)s:%(lineno)s] %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "console",
        },
        "null": {
            "class": "logging.NullHandler",
        },
    },
    "loggers": {
        "": {
            "handlers": ["console"],
            "level": "INFO",
        },
        "django.security.DisallowedHost": {
            "handlers": ["null"],
            "propagate": False,
        },
        "mymodule": {
           "handlers": ["console"],
           "level": "DEBUG",
            "propagate": False,
        },
    },
}

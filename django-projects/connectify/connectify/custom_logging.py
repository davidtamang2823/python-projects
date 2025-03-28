CUSTOM_LOGGING = {
    'version':1,
    'disable_existing_loggers':False,
    'formatters':{
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{'
        },
        'simple':{
            'format': '{levelname} {message}',
            'style': '{'
        }
    },
    'handlers':{
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'verbose',
        }
    },    
    'loggers': {
        'django':{
            'handlers':['console'],
            'level':'DEBUG',
            'propagate':True
        },
    }
}

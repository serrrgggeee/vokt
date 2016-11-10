# EMAIL_BACKEND = 'django_ses.SESBackend'
# AWS_ACCESS_KEY_ID = 'AKIAIW4JARSWEMOZRTOA'
# AWS_SECRET_ACCESS_KEY = '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'
# AWS_SES_REGION_ENDPOINT = 'email.us-east-1.amazonaws.com'
#
# SERVER_EMAIL = "optostack.srv@optoplan.ru"
# DEFAULT_FROM_EMAIL = SERVER_EMAIL


# TMP emailing
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_USE_TLS = True
# EMAIL_HOST = 'smtp.yandex.ru'
# EMAIL_PORT = 587
# EMAIL_HOST_USER = 'optostack@nekidaem.ru'
# EMAIL_HOST_PASSWORD = 'dP7m8Nk92'
# SERVER_EMAIL = "optostack@nekidaem.ru"
# DEFAULT_FROM_EMAIL = SERVER_EMAIL

DEBUG = False
TEMPLATE_DEBUG = False

COMPRESS_ENABLED = True


def modify(settings):
    settings['DATABASES']['default']['HOST'] = '127.0.0.1'
    settings['DATABASES']['default']['PORT'] = '5432'
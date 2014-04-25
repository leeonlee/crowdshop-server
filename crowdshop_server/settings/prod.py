import dj_database_url
DATABASES['default'] = dj_database_url.config(default='postgres://a:a@localhost/crowdshop_server')
DEBUG = False

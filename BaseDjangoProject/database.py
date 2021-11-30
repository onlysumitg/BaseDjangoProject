import environ
import os

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

env = environ.Env()
env.read_env(os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env'))


def get_env_variable(name, default = None, required = True):
    try:
        value = os.getenv(name)
    except KeyError:
        value = env(name)

    if default and value is None:
        value = default

    if required and value is None:
        raise ImproperlyConfigured('Required environment variable "{}" is not set.'.format(name))

    return value


engines = {
    'sqlite': 'django.db.backends.sqlite3',
    'postgresql': 'django.db.backends.postgresql_psycopg2',
    'mysql': 'django.db.backends.mysql',
    'ibmi': 'django_iseries'
}


def config():
    service_name = os.getenv('DATABASE_SERVICE_NAME', '').upper().replace('-', '_')
    if service_name:
        engine = engines.get(os.getenv('DATABASE_ENGINE'), engines['sqlite'])
    else:
        engine = engines['sqlite']

    name = os.getenv('DATABASE_NAME')
    if not name and engine == engines['sqlite']:
        name = os.path.join(settings.BASE_DIR, 'db.sqlite3')

    return {
        'ENGINE': engine,
        'NAME': name,
        'USER': os.getenv('DATABASE_USER'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD'),
        'HOST': os.getenv('{}_SERVICE_HOST'.format(service_name)),
        'PORT': os.getenv('{}_SERVICE_PORT'.format(service_name)),
    }


def ibmi():
    ibmi_host = get_env_variable('IBMI_HOST')
    ibmi_user = get_env_variable('IBMI_USER')
    ibmi_password = get_env_variable('IBMI_PASSWORD')

    engine = engines['ibmi']
    ibmi_libl = get_env_variable('IBMI_LIB', '*USRLIBL').split(' ')  # ['KWDB108', '*USRLIBL']

    return {
        'ENGINE': engine,
        'NAME': 'iseries_2',  # arbitrary database name for db2 on iseries

        'USER': ibmi_user,
        'PASSWORD': ibmi_password,
        'HOST': ibmi_host,
        'OPTIONS': {
            'dbq': ibmi_libl,
            'message_replies': [(17, 'CPA32B2', 'I'), ],
            "nam": 1,
            "cmt": 0,
            'trueautocommit': 0,
            "conn_options": {'autocommit': True},
        }
    }


def pci_db():
    service_name = os.getenv('PCI_DATABASE_SERVICE_NAME', '').upper().replace('-', '_')
    if service_name:
        engine = engines.get(os.getenv('PCI_DATABASE_ENGINE'), engines['sqlite'])
    else:
        engine = engines['sqlite']

    name = os.getenv('PCI_DATABASE_NAME')
    if not name and engine == engines['sqlite']:
        name = os.path.join(settings.BASE_DIR, 'pci_db.sqlite3')

    return {
        'ENGINE': engine,
        'NAME': name,
        'USER': os.getenv('PCI_DATABASE_USER'),
        'PASSWORD': os.getenv('PCI_DATABASE_PASSWORD'),
        'HOST': os.getenv('{}_SERVICE_HOST'.format(service_name)),
        'PORT': os.getenv('{}_SERVICE_PORT'.format(service_name)),
        'SUPPORTS_TRANSACTIONS': True,
    }
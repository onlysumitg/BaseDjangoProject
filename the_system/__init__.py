default_app_config = 'the_system.apps.TheSystemConfig'

""" Avoid duplicate calls """
"""


1. 

When you use python manage.py runserver Django start two processes, one for the actual development server and other to reload your application when the code change.

You can also start the server without the reload option, and you will see only one process running will only be executed once :

python manage.py runserver --noreload



"""


"""
2.

import os

if os.environ.get('RUN_MAIN', None) != 'true':
    default_app_config = 'mydjangoapp.apps.MydjangoappConfig'
"""
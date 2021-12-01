# BaseDjangoProject

## How to use this Project?

- Clone this project

- delete git folder
  - rm -rf .git
  - or manualy

- git init

- git commit -m "First commit"

- create repo on github

- git remote add origin "giturl"

- pipenv install

- python manage.py rename_project NewProject
  - use  --commit option to make the final change

- Have to rename the Top level folder manully.

- python manage.py makemigrations
- python manage.py migrate

- python manage.py createsuperuser

- python manage.py collectstatic



tasks -> https://github.com/codingforentrepreneurs/Guides/blob/master/all/Celery_Redis_with_Django.md


to test celery

Go to pipenv shell

celery -A PayBridge worker -l info --loglevel=DEBUG --without-gossip --without-mingle --without-heartbeat -Ofair --pool=solo



celery -A BaseDjangoProject worker -l info  -Ofair --pool=solo -Q useractivity
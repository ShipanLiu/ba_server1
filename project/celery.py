import os
from celery import Celery

# set an env variable
# we set "DJANGO_SETTINGS_MODULE" mapping to "project.settings"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

# create celery instance, give the name "project
"""
Your Django project folder is named project, but in your Celery configuration, you are initializing Celery with the name project_dj.
These names should be consistent. If your Django project directory (the one containing settings.py) is named project, then you should initialize Celery with project.
"""
celery = Celery("project") # your project name, later in starting terminal you need to give this name

# specify where celery can find the config variables(you need to go to django.config and load the settings module):
# if you set the namespace to "CELERY", then all of our configuration settings should start witl CELERY, see in settings.py
celery.config_from_object("django.conf:settings", namespace="CELERY")


# the celery can auto discover tasks:
celery.autodiscover_tasks()

# to let the celery code work, you need to load the code into '__init__.py' model, otherwise, python will not execute these code.
from __future__ import absolute_import, unicode_literals

# to let python see the celery code:
from.celery import celery as celery_app

"""
The __all__ declaration is a list of public objects of that module, as interpreted by import *. 
It's optional, but it's a good practice to define it, as it provides a clear indication of which 
names are meant to be accessible when this module (__init__.py) is imported.
"""
__all__ = ('celery_app',)

# after this: you need to start a new worker process in the terminal:
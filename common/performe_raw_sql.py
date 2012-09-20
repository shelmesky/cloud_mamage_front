#!/usr/bin/python
import os,sys

# let other can import django's module from outside django
from django.core.management import setup_environ
import settings
setup_environ(settings)

from django.db import connection, transaction



def raw_sql(sql):
    cursor = connection.cursor()
    cursor.execute(sql)
    return cursor
    
    
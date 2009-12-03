"""
This is the mod_wsgi configuration that apache2 uses to interface with
Django and the application.
"""
import os
import sys
# This will quiet the errors when printing but is not ideal.
#sys.stdout = sys.stderr

# Calculate the path based on the location of the WSGI script.
apache_configuration= os.path.dirname(__file__)
project = os.path.dirname(apache_configuration)

# Directory immediately above gchub_db 
if project not in sys.path:
    sys.path.insert(0, project) 

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

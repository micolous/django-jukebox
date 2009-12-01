#!/usr/bin/env python
"""
Scans your media/music directory and adds any new files to the Song DB.
"""
import sys
import os
# Setup the Django environment
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_dir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
# Back to the ordinary imports
from django.conf import settings
from apps.music_db import importer_funcs

print "Scanning %s for new music..." % settings.MUSIC_DIR
importer_funcs.scan_music_dir_for_new_songs()
print "Scan complete."
#!/usr/bin/env python
"""
Starts the audio daemon server. The idea is to check for an SongRequest
objects that have no time_played value. The daemon will play each of these
in order via a simple loop.

juke_daemon has no intelligence other than taking the first request off of the
queue and playing it. Playlist generation is handled by random_requester.py.
"""
import sys
import os
# Setup the Django environment
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_dir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
# Back to the ordinary imports
from django.conf import settings
from twisted.internet import reactor
from apps.juke_daemon import daemon

print "Starting jukebox daemon..."
daemon.daemon_loop()
print "django_jukebox daemon shutdown."
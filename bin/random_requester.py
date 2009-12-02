#!/usr/bin/env python
"""
Randomly fills the anonymous queue with songs. This prevents any dead air
when the actual users haven't requested anything lately.
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
from apps.music_player import random_requester

random_requester.fill_random_request_queue()
"""
Table-level operations.
"""
from django.db import models

class SongRequestManager(models.Manager):   
    def get_pending_anonymous_requests(self):
        """
        Returns a QuerySet of all SongRequest objects that have a None requester
        value. These requests aren't seen as high priority, since they are either
        un-authenticated users or this module's request bot.
        """
        return self.filter(requester__isnull=True, time_played__isnull=True)
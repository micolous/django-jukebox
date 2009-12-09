"""
Table-level operations.
"""
from django.db import models

class SongRequestManager(models.Manager):
    def get_active_requests(self):
        """
        Returns a QuerySet of all SongRequest objects that have not been
        played yet.
        """
        return self.filter(time_played__isnull=True)
    
    def get_pending_user_requests(self):
        """
        Returns all pending requests that were sent by an authenticated User.
        """
        return self.get_active_requests().filter(requester__isnull=False)

    def get_pending_anonymous_requests(self):
        """
        Returns a QuerySet of all SongRequest objects that have a None requester
        value. These requests aren't seen as high priority, since they are either
        un-authenticated users or this module's request bot.
        """
        return self.get_active_requests().filter(requester__isnull=True)
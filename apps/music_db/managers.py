"""
Table-level operations.
"""
from django.db import models
from django.db.models import Q
from django.conf import settings

class SongManager(models.Manager):
    def get_active_requests(self):
        """
        Returns a QuerySet of all SongRequest objects that have not been
        played yet.
        """
        return self.filter(time_played__isnull=True)
    
    def get_good_songs(self):
        """
        Finds all songs that are 'good'.
        """
        # Has minimum good rating and has enough ratings not to be upcoming.
        return self.filter(rating__gte=settings.RANDOM_REQ_GOOD_RATING,
                           num_ratings__gt=settings.RANDOM_REQ_UPCOMING_MAX_RATINGS)
    
    def get_upcoming_songs(self):
        """
        Find all 'upcoming' songs. This means that the songs
        either have no ratings, or only a few, as per capped by
        settings.RANDOM_REQ_UPCOMING_MAX_RATINGS.
        """
        return self.filter(Q(rating__isnull=True) | 
                Q(num_ratings__lte=settings.RANDOM_REQ_UPCOMING_MAX_RATINGS))
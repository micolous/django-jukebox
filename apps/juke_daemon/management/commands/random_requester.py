from django.core.management.base import BaseCommand, CommandError
from apps.music_player import random_requester	

class Command(BaseCommand):
    args = ''
    help = 'Randomly fills the anonymous queue with songs.  This prevents any dead air when the actual users haven\'t requested anything lately.'

    def handle(self, *args, **options):
		self.stdout.write('Randomly filling the anonymous request queue.\n')
		random_requester.fill_random_request_queue()

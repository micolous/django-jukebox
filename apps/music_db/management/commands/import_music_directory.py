from django.core.management.base import BaseCommand, CommandError
from apps.music_db.importer_funcs import scan_dir_for_new_songs
class Command(BaseCommand):
    args = '<directory ...>'
    help = 'Imports some directories in to the music database.'

    def handle(self, *args, **options):
        for directory in args:
			self.stdout.write('Scanning "%s" for music files...\n' % directory)
			scan_dir_for_new_songs(directory, verbose=True)

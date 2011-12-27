from django.core.management.base import BaseCommand, CommandError
try:
	import daemon
	daemon.DaemonContext
except ImportError, AttributeError:
	# you can sort of work without this, but it means it doesn't run nicely as a daemon.
	daemon = None
	
from apps.juke_daemon import daemon as juke_daemon

class Command(BaseCommand):
    args = ''
    help = 'Runs the jukebox daemon.'

    def handle(self, *args, **options):
		self.stdout.write('Starting juke_daemon...\n')
		
		if daemon:
			with daemon.DaemonContext():
				juke_daemon.daemon_loop()
		else:
			self.stderr.write('python-daemon is missing, possibly non-UNIX platform.  Please install it on UNIX platforms.\n')
			juke_daemon.daemon_loop()
		
		self.stdout.write('Stopped juke_daemon...\n')

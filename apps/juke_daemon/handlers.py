"""
This module holds all of the command handlers for the server. For every
incoming packet, the format is: <command> [[arg1] [arg2] [arg3] ...]

The <command> argument will be used with getattr() in the form of
cmd_<command>. So if the <command> argument for a packet is 'lock_job_folder',
the handler will getattr(handlers, cmd_lock_job_folder) and pass any arguments
via the 'args' positional argument.
"""   
def cmd_shutdown(args, server):
    """
    Kill the daemon.
    """
    print "@ Shutting down."
    server.reactor.stop()
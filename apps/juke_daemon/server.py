#!/usr/bin/env python
"""
This is a simple UDP server that listens for UDP datagrams from the 
web front end. Commands are routed to the command handler (handler.py) 
via getattr().
"""
from twisted.internet.protocol import DatagramProtocol
import handlers

class EchoUDP(DatagramProtocol):
    def __init__(self, reactor):
        self.reactor = reactor
               
    def datagramReceived(self, datagram, address):
        """
        Parse the datagram, split it up, and pass it to the correct command
        handler in handlers.py.
        """
        cmd_split = datagram.split()
        #print "SPLIT", cmd_split
        
        cmd_name = cmd_split[0]
        cmd_args = cmd_split[1:]
        cmd_function_str = 'cmd_%s' % cmd_name
        try:
            cmd_func = getattr(handlers, cmd_function_str)
        except AttributeError:
            print "! Invalid command: %s" % cmd_name
            return
            
        cmd_func(cmd_args, self)

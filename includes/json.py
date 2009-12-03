"""
This file contains everything needed to send and receive JSON requests.
"""
from django.utils.functional import Promise
from django.utils import simplejson

class JSMessage(object):
    """
    The JSMessages class is used to pass JSON messages to client JavaScripts.
    Use this as a vessel for JSON stuff instead of directly sending JSON
    text.
    """
    # This is a general message to show the client or to describe the packet.
    message = None
    # Boolean to indicate whether the message is describing an error.
    is_error = False
    # Store strings, dictionary, or list in here for the client to parse.
    contents = None
    
    def __init__(self, message, is_error=False, contents=None):
        """
        Default constructor. Only required argument is message.
        """
        self.message = message
        self.is_error = is_error
        if contents:
            self.contents = contents
            
    def __str__(self):
        """
        The to-string method is called when sending JSMessage objects. This
        is what the client will see.
        """
        # Encode the dictionary and return it for sending.
        return simplejson.dumps({"message": self.message, 
                                 "is_error": self.is_error, 
                                 "contents": self.contents}) 
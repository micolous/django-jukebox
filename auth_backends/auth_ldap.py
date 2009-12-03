"""
LDAP authentication backend. This was developed on Mac OS X's OpenDirectory
implementation, but should work with ActiveDirectory with a little work.
"""
from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend
from django.conf import settings
import ldap

class LDAPBackend(ModelBackend):
    def authenticate(self, username=None, password=None):
        conn = ldap.initialize(settings.LDAP_HOST)
        
        try:
            conn.simple_bind_s(settings.LDAP_USER_BIND_DN % username, password)
        except ldap.INVALID_CREDENTIALS:
            return None
        
        result = conn.search_s(settings.LDAP_USER_BIND_DN % username, 
                               ldap.SCOPE_SUBTREE)
        result_dict = result[0][1]

        #print result_dict.keys()
        #print result_dict.get('sn', 'no sn')
        #print result_dict.get('uidNumber', 'no uidNumber')
        #print result_dict.get('givenName', 'no givenName')
        
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            # givenName == First Name
            if result_dict.has_key('givenName'):
              first_name = result_dict['givenName'][0]
            else:
              first_name = ''
            
            # sn == Last Name (Surname)
            if result_dict.has_key('sn'):
              last_name = result_dict['sn'][0]
            else:
              last_name = ''
            
            # mail == Email Address
            if result_dict.has_key('mail'):
              email = result_dict['mail'][0]
            else:
              email = ''
            
            user = User(username=username,
                        first_name=first_name,
                        last_name=last_name,
                        email=email)
            user.is_staff = False
            user.is_superuser = False
            user.set_password(password)
            user.save()
        return user

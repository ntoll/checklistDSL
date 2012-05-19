"""
An over engineered way of setting the version. Based upon a simplification of
how Django (http://djangoproject.com/) does it. ;-)

Copyright (C) 2012 Nicholas H.Tollervey.
"""

# MAJOR, MINOR, RELEASE, STATUS [alpha, beta, final], VERSION
VERSION = (0, 0, 1, 'alpha', 2)

def get_version():
    """
    Returns a string version of VERSION
    """
    return '.'.join([str(i) for i in VERSION])

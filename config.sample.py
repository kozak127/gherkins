__author__ = 'kozak127'

import os
basedir = os.path.abspath(os.path.dirname(__file__))

CSRF_ENABLED = True

OPENID_PROVIDERS = [
    {'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id'},
    {'name': 'Yahoo', 'url': 'https://me.yahoo.com'},
    {'name': 'AOL', 'url': 'http://openid.aol.com/<username>'},
    {'name': 'Flickr', 'url': 'http://www.flickr.com/<username>'},
    {'name': 'MyOpenID', 'url': 'https://www.myopenid.com'}]


SECRET_KEY = 'sample-secret-key'
SQLALCHEMY_DATABASE_URI = 'mysql://user:password@domain:port/database'
SQLALCHEMY_DATABASE_DEBUG = True

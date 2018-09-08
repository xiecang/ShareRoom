#!/usr/bin/env python3

import sys
from os.path import abspath
from os.path import dirname
import share


sys.path.insert(0, abspath(dirname(__file__)))
application = share.app

"""
ln -s /var/www/bbs/bbs.conf /etc/supervisor/conf.d/bbs.conf

ln -s /var/www/bbs/bbs.nginx /etc/nginx/sites-enabled/bbs

"""

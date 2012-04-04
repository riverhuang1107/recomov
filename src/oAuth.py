#!/usr/bin/env python

import urllib
import random

def escape(s):
    # escape '/' too
    return urllib.quote(s, safe='~')

def generate_nonce(length=8):
    return ''.join([str(random.randint(0, 9)) for i in range(length)])


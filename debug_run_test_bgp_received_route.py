#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os

# arranged print
from pprint import pprint, pformat

# Jinja2 Template Engine
from jinja2 import Template, Environment

# JSNAPy
from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from jnpr.jsnapy import SnapAdmin


jsnapy_config =\
'''
tests:
  - ./tests/test_bgp_advertised_route_192.168.35.2.yml
  - ./tests/test_bgp_received_route_192-168-35-2.yml
''' 
dev1 = Device(
        host = '192.168.34.16',
        user = 'user1',
        password = 'password1')
dev1.open()

jsnapy = SnapAdmin()

snapcheck_dict = jsnapy.snapcheck(
                  data = jsnapy_config,
                  dev = dev1,
                  file_name = "snap01")


print '##### JSNAPy Test : Start #####'
for snapcheck in snapcheck_dict:
    print "Devece : ",         snapcheck.device
    print "Final result : ",   snapcheck.result
    print "Total passed : ",   snapcheck.no_passed
    print "Total failed : ",   snapcheck.no_failed
    print 'snapcheck test_details : '
    print '-'*30
    pprint(dict(snapcheck.test_details)) 
    print '-'*30
print '##### JSNAPy Test : End #####'

dev1.close()
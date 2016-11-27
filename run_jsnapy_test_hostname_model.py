#! /usr/bin/env python
# -*- coding: utf-8 -*-

from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from jnpr.jsnapy import SnapAdmin

from pprint import pprint, pformat

jsnapy_config =\
'''
tests:
- ./tests/test_hostname.yml
- ./tests/test_model.yml
'''

dev1 = Device(
        host = '192.168.34.16',
        user = 'user1',
        password = 'password1',
        port = 22)
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
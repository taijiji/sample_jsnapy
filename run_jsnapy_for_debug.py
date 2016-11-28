# This is debug script for JSNAPy 1.0.0 issue(https://github.com/Juniper/jsnapy/issues/204)
# If you upgrade after JSNAPY 1.0.1, this issue will be solved.

#! /usr/bin/env python
# -*- coding: utf-8 -*-

from jnpr.junos.utils.config import Config
from jnpr.jsnapy import SnapAdmin

jsnapy_config =\
'''
hosts:
  - device: 192.168.34.16 
    username : user1
    passwd: password1
    port: 22
tests:
- ./tests/test_hostname.yml
'''

jsnapy = SnapAdmin()

for i in range(0,10):
    print i
    snapcheck_dict = jsnapy.snapcheck(
                  data = jsnapy_config,
                  file_name = "snap01")
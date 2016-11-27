#! /usr/bin/env python
# -*- coding: utf-8 -*-

from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from jnpr.jsnapy import SnapAdmin

from pprint import pprint, pformat


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

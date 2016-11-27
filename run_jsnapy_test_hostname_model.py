#! /usr/bin/env python
# -*- coding: utf-8 -*-

from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from jnpr.jsnapy import SnapAdmin

dev1 = Device(
        host = '192.168.34.16',
        user = 'user1',
        password = 'password1',
        port = 22)

jsnapy_config =\
'''
tests:
- ./tests/test_hostname.yml
- ./tests/test_model.yml
'''

jsnapy = SnapAdmin()
snapcheck_list = jsnapy.snapcheck(
                  data = jsnapy_config,
                  dev = dev1,
                  file_name = "snap01")




#! /usr/bin/env python
# -*- coding: utf-8 -*-

#from pprint import pprint
from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from jnpr.jsnapy import SnapAdmin


jsnapy = SnapAdmin()


jsnapy_config =\
'''
hosts:
- device: 192.168.34.16
  username: user1
  passwd: password1
  port: 22
tests:
- ./tests/test_hostname.yml
'''

# 知見: snapcheck関数でDeviceクラスを利用するときはhost部は不要 
#dev1 = Device(
#        host = '192.168.34.16',
#        user = 'user1',
#        password = 'password1',
#        port = 22)

print 'test: 1'
snapcheck_list = jsnapy.snapcheck(data=jsnapy_config, file_name="test")

print 'test: 2'
snapcheck_list = jsnapy.snapcheck(data=jsnapy_config, file_name="test")

print 'test: 3'
snapcheck_list = jsnapy.snapcheck(data=jsnapy_config, file_name="test")

print 'test: 4'
snapcheck_list = jsnapy.snapcheck(data=jsnapy_config, file_name="test")

print 'test: 5'
snapcheck_list = jsnapy.snapcheck(data=jsnapy_config, file_name="test")



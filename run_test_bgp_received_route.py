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

template_dir_name  = './test_templates/'
template_base_name = 'test_bgp_received_route.jinja2'
param_received_route = {
    "neighbor_address_ipv4"         : "192.168.35.2",
    "received_route_address_ipv4"   : "10.10.30.0",
    "received_route_subnet_ipv4"    : "24",
}

print 'Load test_template : '
template_filename = template_dir_name + template_base_name
with open(template_filename, 'r') as conf:
    template_txt = conf.read()
    test_yml = Environment().from_string(template_txt).render(param_received_route)
    test_base_name = template_base_name.rstrip('.jinja2') +\
                     '_' + param_received_route["neighbor_address_ipv4"] + '.yml'

test_base_name = test_base_name.rstrip('.yml').replace('.','-') + '.yml'


print 'Test file : '    + test_base_name
print 'Test_yml: '      + test_yml

print 'Save test on ./tests : '
test_dir_name = './tests/'
test_filename = test_dir_name + test_base_name
with open(test_filename, 'w') as f:
    f.write(test_yml)
    print test_filename

jsnapy_config =\
'''
tests:
  - %s
''' % (test_filename)

dev1 = Device(
        host = '192.168.34.16',
        user = 'user1',
        password = 'password1')
dev1.open()

jsnapy = SnapAdmin()

snapcheck_dict = jsnapy.snapcheck( data=jsnapy_config, dev=dev1)

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
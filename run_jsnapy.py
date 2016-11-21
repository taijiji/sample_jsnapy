#! /usr/bin/env python
# -*- coding: utf-8 -*-

#from pprint import pprint
from jnpr.junos import Device
from jnpr.junos.utils.config import Config

from jnpr.jsnapy import SnapAdmin

jsnapy = SnapAdmin()
conf_filename= './config_router1.yml'
jsnapy.snap(conf_filename, "snap1114_01")
print jsnapy.snapcheck(conf_filename, "snap1114_01")




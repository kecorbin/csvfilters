#!/usr/bin/env python

import sys
import csv

sys.path.append('pysdk')
from insieme.mit import access

hostname = sys.argv[1]
username = sys.argv[2]
password = sys.argv[3]
filename = sys.argv[4]
tenant = sys.argv[5]
access.rest()
directory = access.MoDirectory(ip=hostname, port='8000', user=username, password=password)
polUni = directory.lookupByDn('uni')
fvTenant = directory.create('fv.Tenant', polUni, name=tenant)

with open(filename, 'rb') as infile:
     filter_list = csv.reader(infile, delimiter=',',quotechar='|')
     for row in filter_list:
         if row[2] == 'tcp':
            row[2] == 6
         vzFilter = directory.create('vz.Filter', fvTenant, name=row[0])
         vzEntry = directory.create('vz.Entry', vzFilter, etherT=row[1], prot=row[2], dFromPort=row[3], dToPort=row[3], name=row[0]+'-entry')


sd = directory.commit(fvTenant)

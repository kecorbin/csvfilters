#!/usr/bin/env python

import sys
import csv
from argparse import ArgumentParser
sys.path.append('pysdk')
from insieme.mit import access


parser = ArgumentParser(sys.argv[0])
parser.add_argument('-a', '--apic', help='IP Address of APIC', required=True)
parser.add_argument('-u', '--user', help='Username for APIC', required=True)
parser.add_argument('-p', '--password', help='Password of APIC', required=True)
parser.add_argument('-f', '--filename',help='csv containing filter definitions', required=True)
parser.add_argument('-t', '--tenant',help="Tenant Name for filter creation", required=True)
args = parser.parse_args()

hostname = args.apic
username = args.user
password = args.password
filename = args.filename
tenant = args.tenant
access.rest()
directory = access.MoDirectory(ip=hostname, port='8000', user=username, password=password)

def main(directory,filename,tenant):
   directory = access.MoDirectory(ip=hostname, port='8000', user=username, password=password)
   polUni = directory.lookupByDn('uni')
   fvTenant = directory.create('fv.Tenant', polUni, name=tenant)
   
   with open(filename, 'rb') as infile:

        filter_list = csv.reader(infile, delimiter=',',quotechar='|')
        for row in filter_list:
            vzFilter = directory.create('vz.Filter', fvTenant, name=row[0])
            vzEntry = directory.create('vz.Entry', vzFilter, etherT=row[1], prot=row[2], dFromPort=row[3], dToPort=row[3], name=row[0]+'-entry')


	    vzBrCP = directory.create('vz.BrCP', fvTenant, name=row[0]+'-contract')
            vzSubj = directory.create('vz.Subj', vzBrCP, name=row[0]+'-subject')
            vzRsSubjFiltAtt = directory.create('vz.RsSubjFiltAtt', vzSubj, tnVzFilterName=row[0])

   sd = directory.commit(fvTenant)

main(directory,filename,tenant)

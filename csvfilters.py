#!/usr/bin/env python
'''
create tenant filters based on input csv file
updated for build 872
'''

import sys
import csv
from argparse import ArgumentParser
#sys.path.append('~/cobra')
import cobra.mit.access
import cobra.mit.session
import cobra.mit.request
import cobra.model.fv
import cobra.model.vz
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
#cobra.mit.access.access.rest()

ep = cobra.mit.access.EndPoint(hostname, secure=False, port=80)
ls = cobra.mit.session.LoginSession(username,password)
directory = cobra.mit.access.MoDirectory(ep,ls)
directory.login()

def main(directory,filename,tenant):
   polUni = directory.lookupByDn('uni')
   fvTenant = cobra.model.fv.Tenant(polUni, name=tenant)
   
   with open(filename, 'rb') as infile:

        filter_list = csv.reader(infile, delimiter=',',quotechar='|')
        for row in filter_list:
            vzFilter = cobra.model.vz.Filter(fvTenant, name=row[0])
            vzEntry = cobra.model.vz.Entry(vzFilter, etherT=row[1], prot=row[2], dFromPort=row[3], dToPort=row[3], name=row[0]+'-entry')


	    vzBrCP = cobra.model.vz.BrCP(fvTenant, name=row[0]+'-contract')
            vzSubj = cobra.model.vz.Subj(vzBrCP, name=row[0]+'-subject')
            vzRsSubjFiltAtt = cobra.model.vz.RsSubjFiltAtt(vzSubj, tnVzFilterName=row[0])

   c = cobra.mit.request.ConfigRequest()
   c.addMo(polUni)	
   sd = directory.commit(c)

main(directory,filename,tenant)

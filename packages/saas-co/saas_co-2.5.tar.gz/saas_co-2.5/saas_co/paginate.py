import boto3
import pandas as pd
from jsonpath_ng import jsonpath, parse

#####################################

def fields(data, args):
    f = args.get('fields',[])
    if not f: return data
    d = {}
    for je in f: 
        for i in parse(je).find(data):
            d.update({je:i.value})
    return d

#####################################

def found(args,d2):
    f = args.get('filter',[])
    if not f: return True
    for key,val in f.items():
        for i in parse(key).find(d2):
            if i.value in val:
                return True
    return False

#####################################

class paginate():
    def __init__(self, session, **kargs):
        self.json = []
        for page in session.client(kargs.get('service')).get_paginator(kargs.get('ep')).paginate():
            self.json = [fields(i.value, kargs) for i in self.jsonpath_expression().find(page) if found(kargs, i.value)]
        self.df = pd.json_normalize(self.json)

            
    def __str__(self):
        return json.dumps(self.json)

#####################################

class ec2_paginate(paginate):
    def __init__(self, session, **kargs):
        kargs.update({'ep':self.name()})
        kargs.update({'service':'ec2'})
        paginate.__init__(self, session, **kargs)

#####################################

class org_paginate(paginate):
    def __init__(self, session, **kargs):
        kargs.update({'ep':self.name()})
        kargs.update({'service':'organizations'})
        paginate.__init__(self, session, **kargs)

#####################################

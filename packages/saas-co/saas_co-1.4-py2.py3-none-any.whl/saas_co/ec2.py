from jsonpath_ng import parse
from paginate import ec2_paginate as paginate

#####################################

class ec2_describe_instances(paginate):
    def name(self): return __class__.__name__        
    def jsonpath_expression(self): return parse('Reservations[*].Instances[*]')

#####################################

from jsonpath_ng import parse
from .paginate import ec2_paginate

#####################################

class describe_instances(ec2_paginate):
    def name(self): return __class__.__name__        
    def jsonpath_expression(self): return parse('Reservations[*].Instances[*]')

#####################################

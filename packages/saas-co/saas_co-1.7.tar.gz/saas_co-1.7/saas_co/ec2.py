from jsonpath_ng import parse

#####################################

class describe_instances(ec2_paginate):
    def name(self): return __class__.__name__        
    def jsonpath_expression(self): return parse('Reservations[*].Instances[*]')

#####################################

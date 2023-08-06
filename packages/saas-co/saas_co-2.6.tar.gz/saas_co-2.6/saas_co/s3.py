import boto3
from jsonpath_ng import parse
from .paginate import s3_paginate

#####################################

class get_object(s3_paginate):
    def name(self): return __class__.__name__        
    def jsonpath_expression(self): return parse('Body')

#####################################

def put_object(**kargs):
    d = kargs.get('data')
    k = kargs.get('key')
    b = kargs.get('bucket')
    r = kargs.get('region', 'us-east-1')
    boto3.client('s3', r).put_object(Body=d, Bucket=b, Key=k)

#####################################

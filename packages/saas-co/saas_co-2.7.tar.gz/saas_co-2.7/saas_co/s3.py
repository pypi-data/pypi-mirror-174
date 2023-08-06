import boto3

#####################################

def s3_get_object(**kargs):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(kargs.get('bucket'))
    for obj in bucket.objects.all():
        if obj.key == kargs.get('key'):
            return obj.get()['Body'].read()

#####################################

def put_object(**kargs):
    d = kargs.get('data')
    k = kargs.get('key')
    b = kargs.get('bucket')
    r = kargs.get('region', 'us-east-1')
    boto3.client('s3', r).put_object(Body=d, Bucket=b, Key=k)

#####################################

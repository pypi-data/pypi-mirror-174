import awswrangler as wr
from functools import partial

#####################

def query(session, query, **kargs):
    generated_query = generate_query(query, **kargs) 
    return partial(wr.athena.read_sql_query,
                   database=kargs.get('db'),
                   boto3_session=session)(generated_query)

#####################

def generate_query(s, **kargs):
    for key,val in kargs.items():
        s = s.replace('{' + key + '}', str(val)) if f'{key}' in s else s
    return s

#####################


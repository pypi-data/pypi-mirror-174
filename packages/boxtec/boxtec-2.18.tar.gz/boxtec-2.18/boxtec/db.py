import mysql.connector
import requests
from . import api

def get_credentials(api_key, schema='prod'):
    response = requests.get(f"{api.get(schema)}/api/db_credentials", headers={'key': api_key}).json()
    if response['msg'] == 'success':
        return response['data']
    else:
        print(response)
        return None


def get(api_key, schema, buffered=True, dictionary=False):
    credentials = get_credentials(api_key=api_key, schema=schema)
    if not credentials:
        return None, None
    cnx = mysql.connector.connect(
        user=credentials['user'],
        password=credentials['password'],
        host=credentials['host'],
        database=credentials['database']
    )
    
    cur = cnx.cursor(buffered=buffered, dictionary=dictionary)
    return cnx, cur
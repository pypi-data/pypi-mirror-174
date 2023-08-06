import mysql.connector
import requests

APIS = {
  'prod': 'https://api-prod-wwueeaf46q-ey.a.run.app',
  'test': 'https://api-test-wwueeaf46q-ey.a.run.app',
  'dev':'http://127.0.0.1:5002'
}

def get_credentials(api_key, api='prod'):
    response = requests.get(f"{APIS[api]}/api/db_credentials", headers={'key': api_key}).json()
    if response['msg'] == 'success':
        return response['data']
    else:
        print(response)
        return None


def get(api_key, api, buffered=True, dictionary=False):
    credentials = get_credentials(api_key=api_key, api=api)
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
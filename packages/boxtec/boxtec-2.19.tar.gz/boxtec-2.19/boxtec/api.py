APIS = {
  'prod': 'https://api-prod-wwueeaf46q-ey.a.run.app',
  'test': 'https://api-test-wwueeaf46q-ey.a.run.app',
  'dev':'http://127.0.0.1:5002'
}

def get(api):
    if api in APIS:
        return APIS[api]
    else:
        print('api not existent')
        return None
import requests

headers = {'Content-Type': 'application/json'}
data = {'uuid': 'bcf2aa2c',
        'mode': "debug"}
response = requests.post('http://thermostat.labossi.xyz:32826/api/control', json=data, headers=headers)
print(response.json())
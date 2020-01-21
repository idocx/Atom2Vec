import json
import requests
from periodic_table import ELEMENTS

data = {
    'criteria': {
        'elements': {'$in': ELEMENTS},
        'nelements': 2,
    },
    'properties': [
        'formula',
    ]
}
r = requests.post('https://materialsproject.org/rest/v2/query',
                 headers={'X-API-KEY': "<your mp key>"},
                 data={k: json.dumps(v) for k,v in data.items()})

response_content = r.json() # a dict

with open("string_2.json", "w") as f:
    json.dump(response_content, f)

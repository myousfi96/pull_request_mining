
import requests
import os
from pprint import pprint
import json

token = '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'
owner = "ansible"
repo = "ansible"
query_url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
complete_data = []
for i in range(1):
    params = {
        "per_page": 30,
        "page": 10
    }
    headers = {'Authorization': f'token {token}'}
    r = requests.get(query_url, headers=headers, params=params)
    data = r.json()
    pprint(data)


#
# with open("pulls.json", "w") as outfile:
#     json.dump(complete_data, outfile)
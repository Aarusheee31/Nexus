import requests

url = "https://api.foodoscope.com/flavordb/entities/by-entity-alias-readable"

params = {
    "entity_alias_readable": "orange"
}

headers = {
    "Authorization": "Bearer Y2OYhJpk2OjKmCic-fmVCm_BPXuhBc2N75hZukqjQstOyFPF",
}

response = requests.get(url, params=params, headers=headers)

print(response.status_code)
print(response.text)   # <-- NOT response.json() yet

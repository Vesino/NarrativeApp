import requests

def get_assets(asset, year, month, day):
    url = 'http://localhost:8000/assets/' 
    params = {'asset':asset,'year': year,'month':month, 'day':day}
    r = requests.get(url, params=params)
    assets = r.json()
    assets_list = {'assets':assets['results']}
    return assets_list
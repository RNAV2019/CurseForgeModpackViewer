from dotenv import load_dotenv
import requests
import zipfile
import io
import json
import os

load_dotenv()
api_key = os.getenv('API_KEY')

headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    # Enter your curseforge api key here
    'x-api-key': api_key
}

mods = input('What is the id of the modpack that you would like the list of: ')
base_url = 'https://api.curseforge.com'

if (os.listdir(os.getcwd()).count(mods) == 0):
    modIds = {'modIds': [mods]}
    r = requests.post(f'{base_url}/v1/mods', headers=headers, json=modIds)
    print(r.json()['data'][0]['latestFiles'][0]['downloadUrl'])
    downloadURL = r.json()['data'][0]['latestFiles'][0]['downloadUrl']
    r2 = requests.get(downloadURL)
    z = zipfile.ZipFile(io.BytesIO(r2.content))
    z.extractall(mods)
    mod_data = ''
    mod_name = ''

with open(f'{os.getcwd()}/{mods}/manifest.json', 'r') as f:
    data = json.load(f)
    for i in range(len(data['files'])):
        mod_data = requests.get(
            f'{base_url}/v1/mods/{data["files"][i]["projectID"]}', headers=headers)
        mod_name = mod_data.json()['data']['name']
        print(mod_name)

print(
    f'There are {len(data["files"])} mods in {data["name"]}')

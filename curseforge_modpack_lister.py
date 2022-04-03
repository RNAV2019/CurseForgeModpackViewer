import requests, zipfile, io, json, os

# Works with windows only
curr_user = os.getlogin()

headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
  'x-api-key': '' # Enter your curseforge api key here
}

mods = input('What is the id of the modpack that you would like the list of: ')

modIds = {'modIds': [mods]}

base_url = 'https://api.curseforge.com'

r = requests.post(f'{base_url}/v1/mods', headers=headers, json=modIds)

print(r.json()['data'][0]['latestFiles'][0]['downloadUrl'])
downloadURL = r.json()['data'][0]['latestFiles'][0]['downloadUrl']

r2 = requests.get(downloadURL)
z = zipfile.ZipFile(io.BytesIO(r2.content))
extracted_path = f'C:\\Users\\{curr_user}\\Desktop\\extracted'
z.extractall(extracted_path)

mod_data = ''
mod_name = ''

with open(f'{extracted_path}\\manifest.json', 'r') as f:
  data = json.load(f)
  print(f'There are {len(data["files"])} mods in {r.json()["data"][0]["name"]}')
  for i in range(len(data['files'])):
    mod_data = requests.get(f'{base_url}/v1/mods/{data["files"][i]["projectID"]}', headers=headers)
    mod_name = mod_data.json()['data']['name']
    print(mod_name)
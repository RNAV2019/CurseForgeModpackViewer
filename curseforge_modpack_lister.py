from tkinter.constants import E, EW, N, NE, NW, W
from dotenv import load_dotenv
import tkinter
import requests
import zipfile
import io
import json
import os

load_dotenv()
api_key = os.getenv("API_KEY")
wn = tkinter.Tk()

headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    # Enter your curseforge api key here
    "x-api-key": api_key,
}


def get_mods_from_modpack():
    mods = project_id_entry.get()
    if mods.isnumeric() == False:
        return None
    # mods = input("What is the id of the modpack that you would like the list of: ")
    base_url = "https://api.curseforge.com"

    if os.listdir(os.getcwd()).count(mods) == 0:
        modIds = {"modIds": [mods]}
        r = requests.post(f"{base_url}/v1/mods", headers=headers, json=modIds)
        print(r.json()["data"][0]["latestFiles"][0]["downloadUrl"])
        downloadURL = r.json()["data"][0]["latestFiles"][0]["downloadUrl"]
        r2 = requests.get(downloadURL)
        z = zipfile.ZipFile(io.BytesIO(r2.content))
        z.extractall(mods)
        mod_data = ""
        mod_name = ""

    with open(f"{os.getcwd()}/{mods}/manifest.json", "r") as f:
        data = json.load(f)
        for i in range(len(data["files"])):
            mod_data = requests.get(
                f'{base_url}/v1/mods/{data["files"][i]["projectID"]}', headers=headers
            )
            mod_name = mod_data.json()["data"]["name"]
            print(mod_name)

    print(f'There are {len(data["files"])} mods in {data["name"]}')
    return None


wn.geometry("600x400")

project_frame = tkinter.Frame(wn)
project_frame.grid(row=1)
project_id_label = tkinter.Label(wn, text="Project ID:")
project_id_label.grid(row=0, column=0)
project_id_entry = tkinter.Entry(project_frame, width=15)
project_id_entry.grid(row=1, column=0)
project_id_submit = tkinter.Button(
    project_frame, text="Submit", width=5, command=get_mods_from_modpack
)
project_id_submit.grid(row=1, column=1)

wn.mainloop()

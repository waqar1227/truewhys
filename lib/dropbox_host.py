"""Temporary public hosting for cross-post media (Metricool needs a public URL).

python lib/dropbox_host.py up <file> [<dropbox name>]   -> prints a direct-download URL (dl=1)
python lib/dropbox_host.py rm <dropbox name>            -> deletes the file once it is posted

The Dropbox token is a network secret injected by the proxy for content.dropboxapi.com / api.dropboxapi.com;
this script never sees or sends it. Files go to the app folder root.
"""
import sys, json
from pathlib import Path
import requests

H = {"Authorization": "Bearer proxy-injected"}  # placeholder: the proxy replaces it


def up(path, name=None):
    name = "/" + (name or Path(path).name)
    with open(path, "rb") as f:
        r = requests.post("https://content.dropboxapi.com/2/files/upload", data=f, timeout=600,
                          headers={**H, "Content-Type": "application/octet-stream",
                                   "Dropbox-API-Arg": json.dumps({"path": name, "mode": "overwrite"})})
    r.raise_for_status()
    r = requests.post("https://api.dropboxapi.com/2/sharing/create_shared_link_with_settings", json={"path": name}, headers=H, timeout=60)
    if r.status_code == 409:  # link already exists
        r = requests.post("https://api.dropboxapi.com/2/sharing/list_shared_links", json={"path": name, "direct_only": True}, headers=H, timeout=60)
        r.raise_for_status()
        url = r.json()["links"][0]["url"]
    else:
        r.raise_for_status()
        url = r.json()["url"]
    return url.replace("dl=0", "dl=1")


def rm(name):
    r = requests.post("https://api.dropboxapi.com/2/files/delete_v2", json={"path": "/" + name.lstrip("/")}, headers=H, timeout=60)
    return r.status_code in (200, 409)


if __name__ == "__main__":
    if sys.argv[1] == "up":
        print(up(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None))
    elif sys.argv[1] == "rm":
        print("deleted" if rm(sys.argv[2]) else "failed")

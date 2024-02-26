#!/usr/bin/python

import os
import socket
import subprocess
import json
import sys

# Command for get ocupped workspaces

# OBS I try use picke but does not working :(, improve loading cached filed 

CACHE_PATH = "/tmp/workspaces.cache"

OCUPPED_WORKSPACES = "hyprctl workspaces -j | jq -c -r '.[] | select(.windows > 0)' | jq -c -r \".id\" | sort "
CURRENT_WORKSPACE = "hyprctl activeworkspace -j | jq '.id'"

URGENT_WORKSPACE = lambda addr: f"hyprctl clients -j | jq -c -r '.[] | select(.address == \"0x{addr}\")' | jq \".workspace\" | jq \".id\""

WORKSPACE_NUMBER = 10


cached_content = []

class Cache:
    def __init__(self, cache_file=CACHE_PATH):
        self.cache_file = cache_file

    def get(self):
        try:
            with open(self.cache_file, 'r') as f:
                content = []
                for i in f.read().splitlines():
                   content.append(i)
                return content
        except FileNotFoundError:
            return []

    def save(self, content: list):
        with open(self.cache_file, 'w') as f:
            for line in content:
                f.write(str(line) + '\n')

# class Cache:
#     def __init__(self, cache_file=CACHE_PATH):
#         self.cache_file = cache_file
#
#     def get(self):
#         with open(self.cache_file, 'r') as f:
#             return f.read().splitlines() if os.path.isfile(self.cache_file) else []
#
#     def save(self, content: list):
#         with open(self.cache_file, 'w') as f:
#             f.write('\n'.join(map(str, content)))


def run_command(command: str):
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output = result.stdout.strip()
        
        return {"data": output}
        
    except subprocess.CalledProcessError as e:
        return {"data": e.stderr.strip()}

def get_ocupped_workspaces():
   return run_command(OCUPPED_WORKSPACES)["data"]

def get_active_workspace():
    return run_command(CURRENT_WORKSPACE)["data"]

def get_urgent_workspace(window_id:str):
    return run_command(URGENT_WORKSPACE(window_id))["data"]

def jdumps(content):
    return json.dumps(content)

def eww_update(value):
    run_command(f"eww update workspaces={jdumps(value)}")

def urgent_mount(event: str):
    c = Cache()
    cached_content = c.get()

    # Referência ao workspace urgente

    window_id = event.split(">>")[1]
    ugt_workspace = get_urgent_workspace(window_id)

    if ugt_workspace not in cached_content:
        cached_content.append(ugt_workspace)
        c.save(cached_content)

    mount_workspace()


def mount_workspace():
    x = []
    c = Cache()


    wcurrent = get_active_workspace()
    busy_workspaces = get_ocupped_workspaces().split("\n")

    cached_content = c.get()
    
    if(wcurrent in cached_content):
        index = cached_content.index(wcurrent)
        cached_content.pop(index)
        c.save(cached_content) 

    for i in range(1, WORKSPACE_NUMBER + 1):
        x.append(
            {
                "id": f"{i}",
                "active": 1 if wcurrent == str(i) else 0,    
                "busy": 1 if str(i) in busy_workspaces and str(i) != wcurrent else 0, 
                "urgent": 1 if str(i) in cached_content and str(i) != wcurrent else 0
            }
        ) 

    eww_update(jdumps(x)) 

def handler(): 
    sp = f"/tmp/hypr/{os.environ['HYPRLAND_INSTANCE_SIGNATURE']}/.socket2.sock"
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

    s.connect(sp)
    while True:
        event = s.recv(1024).decode().strip()

        if event.startswith("workspace") or event.startswith("focusedmon"):
            mount_workspace()

        if event.startswith("urgent"):
            urgent_mount(event)
      

if __name__ == "__main__":
    if sys.argv[1] == "":
        mount_workspace()

    if sys.argv[1] == "urgent":
        urgent_mount(sys.argv[2])


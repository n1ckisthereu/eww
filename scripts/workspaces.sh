#!/bin/bash

scripts/workspaces.py ""

socat -u UNIX-CONNECT:/tmp/hypr/"$HYPRLAND_INSTANCE_SIGNATURE"/.socket2.sock - | while read -r event; do
	if [[ ${event:0:9} == "workspace" ]]; then
		scripts/workspaces.py ""
	fi

	if [[ ${event:0:10} == "focusedmon" ]]; then
		scripts/workspaces.py ""
	fi

	if [[ ${event:0:6} == "urgent" ]]; then
		scripts/workspaces.py "urgent" "$event"
	fi
done

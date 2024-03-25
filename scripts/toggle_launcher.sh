#!/bin/bash

state=$(eww get open_launcher)

eww open launcher --toggle

open_launcher() {
	if [[ -z $(eww active-windows | grep '*launcher') ]]; then
		eww open launcher
	fi
	eww update open_launcher=true
	sleep 0.5 && scripts/apps.py &
}

close_launcher() {
	# eww close launcher
	eww update open_launcher=false
	scripts/apps.py &
}

case $1 in
close)
	close_launcher
	exit 0
	;;
open)
	open_launcher
	exit 0
	;;
esac

case $state in
true)
	close_launcher
	exit 0
	;;
false)
	open_launcher
	exit 0
	;;
esac

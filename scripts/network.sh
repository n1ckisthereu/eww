#!/bin/bash

function wired_connection {
	while true; do
		isconn=$(echo $(nmcli -f TYPE device | awk 'NR >= 2' | grep -v 'loopback' | head -n1) | tr -d "\n")

		if [ "$isconn" == "ethernet" ]; then
			status=$(echo $(nmcli networking connectivity check) | tr -d "\n")

			if [ "$status" = "full" ]; then
				echo '{"connstatus": "full"}'
			elif [ "$status" = "limited" ]; then
				echo '{"connstatus": "limited"}'
			elif [ "$status" = "none" ]; then
				echo '{"connstatus": "none"}'
			fi
		fi

		sleep 5
	done
}

function is_wifi {
	while true; do
		iswifi=$(echo $(nmcli -f TYPE device | awk 'NR >= 2' | grep -v 'loopback' | head -n1) | tr -d "\n")

		if [ "$iswifi" = "wifi" ]; then
			echo "true"
		else
			echo "false"
		fi
		sleep 2
	done
}

function monitor_wifi {
	signal=$(nmcli -f in-use,signal dev wifi | rg "\*" | awk '{ print $2 }')
	essid=$(nmcli -t -f NAME connection show --active | head -n1 | sed 's/\"/\\"/g')
	echo '{"essid": "'"$essid"'", "signal": "'"$signal"'"}'

	while true; do
		signal=$(nmcli -f in-use,signal dev wifi | rg "\*" | awk '{ print $2 }')
		essid=$(nmcli -t -f NAME connection show --active | head -n1 | sed 's/\"/\\"/g')
		echo '{"essid": "'"$essid"'", "signal": "'"$signal"'"}'
		sleep 2
	done
}

if [ "$1" == "wifi-monitor" ]; then
	monitor_wifi
elif [ "$1" == "is-wifi" ]; then
	is_wifi
elif [ "$1" == "wired-connection" ]; then
	wired_connection
fi

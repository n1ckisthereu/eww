#!/bin/bash

state=$(eww get open_calendar)
state_control_center=$(eww get open_control_center)

open_calendar() {
	if [[ -z $(eww active-windows | grep 'calendar_indicator') ]]; then
		eww open calendar_indicator
	fi
	eww update open_calendar=true

	if [[ "$state_control_center" == true ]]; then
		eww update open_control_center=false
	fi
}

close_calendar() {
	eww update open_calendar=false
	sleep 0.2
	eww close calendar_indicator
}

case $1 in
close)
	close_calendar
	exit 0
	;;
esac

case $state in
true)
	close_calendar
	;;
false)
	open_calendar
	;;
esac

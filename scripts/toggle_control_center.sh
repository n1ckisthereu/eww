#!/bin/bash

state=$(eww get open_control_center)
state_calendar=$(eww get open_calendar)

open_control_center() {
	if [[ -z $(eww active-windows | grep 'control_center') ]]; then
		eww open control_center
	fi
	eww update open_control_center=true

	if [[ "$state_calendar" == true ]]; then
		eww update open_calendar=false
	fi
}

close_control_center() {
	eww update open_control_center=false
}

case $1 in
close)
	close_control_center
	exit 0
	;;
esac

case $state in
true)
	close_control_center
	;;
false)
	open_control_center
	;;
esac

# state=$(eww get open_control_center)
#
# open_control_center() {
# 	eww open control_center
# 	eww update open_control_center=true
# }
#
# close_control_center() {
# 	eww update open_control_center=false
# 	sleep 2
# 	eww close control_center
# }
#
# case $state in
# true)
# 	close_control_center
# 	;;
# false)
# 	open_control_center
# 	;;
# esac

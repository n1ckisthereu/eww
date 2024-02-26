#!/bin/bash
pkill eww
pkill notifications

/home/nick/.config/eww/scripts/monitor_width.sh &

eww daemon

eww open bar --arg size=$(eww get monitor_width)
#eww open bg_widgets
eww open notifications_popup
/home/nick/.config/eww/scripts/notifications.py &

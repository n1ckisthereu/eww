#!/bin/bash

monitor_width=$(hyprctl monitors -j | jq -r ".[]" | jq ".width" | head -n 1)

eww update monitor_width="$(echo "scale=2; $monitor_width * 0.98" | bc)px"

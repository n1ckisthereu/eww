while true; do
	is_shared=$(timeout 0.1 pw-top -b)

	if echo "$is_shared" | grep -qE '[0-9]+x[0-9]+.*xdg-desktop-portal-hyprland'; then
		echo "true"
	elif pgrep wf-recorder >/dev/null; then
		echo "true"
	else
		echo "false"
	fi

	sleep 5
done

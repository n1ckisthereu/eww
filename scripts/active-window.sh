previous_title=""

getBox() {
	local content=""

	title=$(hyprctl activewindow -j | jq -r '.title')
	app=$(ps -p $(hyprctl activewindow -j | jq -r '.pid') -o comm=)

	if [[ $title != $previous_title ]]; then
		if [[ $title == null || $app == null ]]; then
			content="💻 Desktop"
		elif [[ "${title:0:3}" == "OBS" ]]; then
			content="${app} - OBS Studio"
		else
			toshow="$app - $title"
			maxlen=30
			sufix=""

			if test $(echo $toshow | wc -c) -ge $maxlen; then
				sufix=" ..."
			fi

			content="${toshow:0:$maxlen}$sufix"
		fi

		echo "(box :class \"active-window\" (label :text \"$content\" :class \"wintitle\")  ) "
		previous_title=$title
	fi

	#echo $content
}

getTitle() {
	if [[ ${1:0:12} == "activewindow" ]]; then
		getBox
	fi

}

getBox

socat -u UNIX-CONNECT:/tmp/hypr/"$HYPRLAND_INSTANCE_SIGNATURE"/.socket2.sock - | while read -r event; do
	getTitle $event
done

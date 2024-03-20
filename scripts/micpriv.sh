while true; do
	result=$(lsof /dev/snd/pcm*c)

	if [ -n "$result" ]; then
		echo "true"
	else
		echo "false"
	fi

	sleep 2
done

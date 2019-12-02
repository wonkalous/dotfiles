#!/usr/bin/env bash
WS_NUM=$(i3-msg -t get_workspaces\
    |jq '.[] | select(.focused==true).num'\
    );

NEW=$(($WS_NUM + 1));

# if (($NEW % 10 == 5))
# then
# 	NEW=$(($NEW + 1))
# fi

# if (($WS_NUM % 10 != 5))
# then
	i3-msg rename workspace $NEW to "temp";
	i3-msg rename workspace $WS_NUM to $NEW;
	i3-msg rename workspace "temp" to $WS_NUM;
# fi

# get name and number of current, save name and change number, get name of exchanged slot and preserve
# OR just skip over main (5th) workspace
# TODO: also switch names, if at _5 make sure there is a placeholder, and also in container move scripts, 
#!/usr/bin/env bash
WS_NUM=$(i3-msg -t get_workspaces\
    |jq '.[] | select(.focused==true).name'\
    |sed 's/\"\([0-9]*\).*/\1/');

NEW=$(($WS_NUM - 1));

# if (($NEW % 10 == 5))
# then
# 	NEW=$(($NEW - 1))
# fi

# if (($WS_NUM % 10 != 5))
# then
	i3-msg rename workspace $NEW to "temp";
	i3-msg rename workspace $WS_NUM to $NEW;
	i3-msg rename workspace "temp" to $WS_NUM;
# fi
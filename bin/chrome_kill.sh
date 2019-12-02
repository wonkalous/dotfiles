#!/usr/bin/env bash
WS_NUM=$(i3-msg -t get_workspaces\
    |jq '.[] | select(.focused==true).name'\
    |sed 's/\"\([0-9]*\).*/\1/');

kill $(ps x | grep "\/chrome *.* --type=renderer .*temp/c$((($WS_NUM-$WS_NUM%10)/10))" | awk '{print $1}')
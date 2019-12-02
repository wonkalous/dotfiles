#!/usr/bin/env bash
# i3-msg move container to workspace number \
#     $((1+`i3-msg -t get_workspaces\
#     | jq '.[] | select(.focused==true).num'`))
#     # | sed 's/\"\([0-9]*\).*/\1+1/'`))

WS_NUM=$(i3-msg -t get_workspaces|jq '.[] | select(.focused==true).num')

NEW=$(($WS_NUM + 1));

i3-msg move container to workspace number $NEW
i3-msg workspace number $NEW


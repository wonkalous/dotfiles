#!/usr/bin/env bash
i3-msg workspace number \
    $((`i3-msg -t get_workspaces\
    |jq '.[] | select(.focused==true).name'\
    |sed 's/\"\([0-9]*\).*/\1+1/'`))

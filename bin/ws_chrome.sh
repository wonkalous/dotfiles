#!/usr/bin/env bash
google-chrome --user-data-dir=$HOME/temp/c\
`i3-msg -t get_workspaces\
    |jq '.[] | select(.focused==true).name'\
    |cut -d "\"" -f2 \
    |sed 's/\([0-9]\).*/\1/'`
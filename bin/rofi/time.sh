#!/usr/bin/env bash

style="$HOME/.dotfiles/bin/rofi/time.rasi"
rofi_command="rofi -theme $style"

## Get time and date
TIME="$(date +"%I:%M %p")"
DN=$(date +"%A")
MN=$(date +"%B")
DAY="$(date +"%d")"
MONTH="$(date +"%m")"
YEAR="$(date +"%Y")"


## Main
$rofi_command -p "   $DN, $TIME" -dmenu
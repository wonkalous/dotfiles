#!/usr/bin/env bash

wget -qO - https://download.sublimetext.com/sublimehq-pub.gpg | sudo apt-key add -
apt sudo-get install apt-transport-https
if grep -q sublimetext /etc/apt/sources.list.d/sublime-text.list; then
    echo sublime source already there
else
	echo "deb https://download.sublimetext.com/ apt/stable/" | sudo tee /etc/apt/sources.list.d/sublime-text.list
fi
sudo apt update
sudo apt install i3


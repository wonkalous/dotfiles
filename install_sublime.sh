#!/usr/bin/env bash


if grep -q sublimetext /etc/apt/sources.list.d/sublime-text.list; then
    echo sublime already installed
else
	wget -qO - https://download.sublimetext.com/sublimehq-pub.gpg | sudo apt-key add -
	apt sudo-get install apt-transport-https
	echo "deb https://download.sublimetext.com/ apt/stable/" | sudo tee /etc/apt/sources.list.d/sublime-text.list
	sudo apt-get update
	sudo apt-get install sublime-text
	mkdir -p  ~/.config/sublime-text-3
	wget -P ~/.config/sublime-text-3/Installed\ Packages https://packagecontrol.io/Package%20Control.sublime-package
fi

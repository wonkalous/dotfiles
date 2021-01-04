cd ~/code
git clone git@github.com:cdown/clipmenu.git
git clone git@github.com:cdown/clipnotify.git

sudo apt install gcc libx11-dev libxfixes-dev xsel
cd clipnotify
sudo make install
cd clipmenu
sudo make install

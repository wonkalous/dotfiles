cd ~/code
git clone git@github.com:svenstaro/rofi-calc.git
sudo apt -y install rofi-dev qalc libtool

cd ~/code/rofi-calc
autoreconf -i
mkdir build
cd ~/code/rofi-calc/build/
../configure
make
make install
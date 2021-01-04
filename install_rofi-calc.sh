cd ~/code
git clone git@github.com:svenstaro/rofi-calc.git
sudo apt install rofi-dev qalc libtool

cd rofi-calc
autoreconf -i
mkdir build
cd build/
../configure
make
make install
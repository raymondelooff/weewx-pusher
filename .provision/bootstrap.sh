#!/bin/sh

WEEWX_VERSION="3.5.0"

# Install required packages
sudo apt-get -y install python-configobj python-cheetah python-imaging python-pip

# Install Pusher
pip install pusher

# Build WeeWX
cd /home/vagrant
wget http://weewx.com/downloads/weewx-${WEEWX_VERSION}.tar.gz
tar xvfz weewx-${WEEWX_VERSION}.tar.gz
cd weewx-${WEEWX_VERSION}
./setup.py build

# Install WeeWX
cd /home/vagrant
cd weewx-${WEEWX_VERSION}
sudo ./setup.py install --no-prompt

# Run WeeWX as a daemon
cd /home/weewx
sudo cp util/init.d/weewx.debian /etc/init.d/weewx
sudo chmod +x /etc/init.d/weewx
sudo update-rc.d weewx defaults 98

# Move configuration
rm /home/weewx/weewx.conf
mv /home/vagrant/weewx.conf /home/weewx/weewx.conf

# Start WeeWX
sudo /etc/init.d/weewx start



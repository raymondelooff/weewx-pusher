#!/bin/bash

PYTHON_VERSION="2.7.15"
WEEWX_VERSION="3.8.0"

echo '
export LC_ALL=C' >> ~/.bashrc

# Update packages and install build packages
# https://github.com/pyenv/pyenv/wiki/Common-build-problems
sudo apt-get update
sudo apt-get dist-upgrade

sudo apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev \
libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
xz-utils tk-dev

# Install pyenv
curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash

echo '
export PATH="~/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc

PATH="~/.pyenv/bin:$PATH"
eval "$(pyenv init -)"

pyenv install $PYTHON_VERSION
pyenv global $PYTHON_VERSION

# Install dependencies
pip install --upgrade pip
pip install configobj Cheetah pillow pusher

# Build and install WeeWX
wget http://weewx.com/downloads/weewx-${WEEWX_VERSION}.tar.gz
tar xvfz weewx-${WEEWX_VERSION}.tar.gz
cd weewx-${WEEWX_VERSION}
./setup.py build

sed -i -e 's/\/home\/weewx/\/home\/vagrant/g' setup.cfg
./setup.py install --no-prompt

cd ~
rm -r weewx-${WEEWX_VERSION}*

echo '
export PATH="~/bin:$PATH"' >> ~/.bashrc

# Link project
ln -s /home/vagrant/weewx-pusher/bin/user/pusher_.py /home/vagrant/bin/user/pusher_.py

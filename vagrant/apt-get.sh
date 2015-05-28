#! /usr/bin/env bash

set -u  # exit if using uninitialised variable
set -e  # exit if some command in this script fails
trap "echo $0 failed because a command in the script failed" ERR


# Install apt-get packages

sed -e 's/archive.ubuntu.com/de.archive.ubuntu.com/g' -i /etc/apt/sources.list

# Install Google Chrome: web-component-tester doesn't detect Chromium
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add -
echo "deb http://dl.google.com/linux/chrome/deb/ stable main " > /etc/apt/sources.list.d/google.list

apt-get update
apt-get install -y \
	build-essential vim htop \
	apache2 libapache2-mod-auth-pubtkt libapache2-mod-wsgi-py3 \
	rabbitmq-server python3 python3-pip python-virtualenv \
	supervisor postgresql libpq-dev python-dev \
	npm git \
	xvfb chromium-browser chromium-chromedriver firefox \
	default-jre google-chrome-stable
# Use python3-virtualenv instead, in distributions that have it
# default-jre is added because ‘wct’ uses Java
# google-chrome-stable because web-component-tester doesn't detect Chromium

# bower complains (on usage) '/usr/bin/env: node: No such file or directory'
ln -s /usr/bin/nodejs /usr/bin/node

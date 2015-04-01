#! /usr/bin/env bash

set -u  # exit if using uninitialised variable
set -e  # exit if some command in this script fails
trap "echo $0 failed because a command in the script failed" ERR


ROOT_DIR=/vagrant/vagrant

"$ROOT_DIR"/set-nameservers.sh
"$ROOT_DIR"/npm.sh

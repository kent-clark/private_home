#!/bin/bash
cd "$(dirname "$0")"

pip3 install python-kasa --pre
pyinstaller --copy-metadata=python-kasa -y ../my_home.py
cp private_home.desktop ~/.local/share/applications

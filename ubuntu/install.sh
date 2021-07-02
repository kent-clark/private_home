#!/bin/bash
cd "$(dirname "$0")"

pip3 install python-kasa --pre
pyinstaller --copy-metadata=python-kasa -y ../main.py
cp xhome.desktop ~/.local/share/applications

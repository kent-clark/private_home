#!/bin/bash
cd "$(dirname "$0")"
cd ..

cp ./macos/setup.py .
python3 setup.py py2app -A
rm setup.py

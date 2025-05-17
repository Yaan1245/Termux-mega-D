#!/data/data/com.termux/files/usr/bin/bash

echo "Updating Termux packages..."
pkg update -y && pkg upgrade -y

echo "Installing required packages: python, git, megacmd..."
pkg install -y python git megacmd

echo "Setting up Termux storage..."
termux-setup-storage

cd ~
echo "permission to run"
cd ~/Termux-mega-D
chmod 
chmod 777 *

echo "Setup complete!"
echo "You can now run your Mega downloader Python script my givem command==== ."
echo "python megadl.py"

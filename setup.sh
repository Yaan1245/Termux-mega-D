#!/data/data/com.termux/files/usr/bin/bash

echo "Updating Termux packages..."
pkg update -y && pkg upgrade -y

echo "Installing required packages: python, git, megacmd..."
pkg install -y python git megacmd

echo "Setting up Termux storage..."
termux-setup-storage

cd ~
echo "Permission to run"
cd ~/Termux-mega-D

# Make sure to set permissions properly
chmod 777 *

echo "Setup complete!"
echo "You can now run your Mega downloader Python script."
echo "Running python megadl.py now..."

python megadl.py

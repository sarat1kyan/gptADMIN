#!/bin/bash

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "You need to run this script as root."
    exit 1
fi

# Determine the package manager
if [ -x "$(command -v apt-get)" ]; then
    package_manager="apt-get"
elif [ -x "$(command -v dnf)" ]; then
    package_manager="dnf"
elif [ -x "$(command -v yum)" ]; then
    package_manager="yum"
elif [ -x "$(command -v zypper)" ]; then
    package_manager="zypper"
elif [ -x "$(command -v pacman)" ]; then
    package_manager="pacman"
elif [ -x "$(command -v apk)" ]; then
    package_manager="apk"
elif [ -x "$(command -v eopkg)" ]; then
    package_manager="eopkg"
elif [ -x "$(command -v xbps-install)" ]; then
    package_manager="xbps-install"
elif [ -x "$(command -v pisi)" ]; then
    package_manager="pisi"
elif [ -x "$(command -v swupd)" ]; then
    package_manager="swupd"
else
    echo "Unsupported package manager. Please install required packages manually."
    exit 1
fi

# Install required packages
echo "Installing required packages..."
case $package_manager in
    "apt-get")
        sudo $package_manager update
        sudo $package_manager install -y python3 python3-pip
        ;;
    "dnf" | "yum")
        sudo $package_manager install -y python3 python3-pip
        ;;
    "zypper")
        sudo $package_manager install -y python3 python3-pip
        ;;
    "pacman")
        sudo $package_manager -Syu python python-pip
        ;;
    "apk")
        sudo $package_manager add python3 py3-pip
        ;;
    "eopkg")
        sudo $package_manager install -y python3 python3-pip
        ;;
    "xbps-install")
        sudo $package_manager -S python3 python3-pip
        ;;
    "pisi")
        sudo $package_manager install -y python3 python3-pip
        ;;
    "swupd")
        sudo $package_manager bundle-add python3-basic
        ;;
esac

# Install Python packages
echo "Installing Python packages..."
pip3 install openai os re time platform

# Prompt user for OpenAI API key
read -p "Enter your OpenAI API key: " api_key
export OPENAI_API_KEY=$api_key

echo "Script execution completed."
echo "gptADMIN dependencies satisfied so now you can run gptADMIN.py, have a nice day."

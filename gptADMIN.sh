#!/bin/bash

# Colors for output
GREEN="\e[32m"
RED="\e[31m"
YELLOW="\e[33m"
CYAN="\e[36m"
BOLD="\e[1m"
RESET="\e[0m"

# Check for root privileges
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}${BOLD}[ERROR] You need to run this script as root.${RESET}"
    exit 1
fi

# Detect package manager
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
    echo -e "${RED}[ERROR] Unsupported package manager or Linux distribution. Please install required packages manually.${RESET}"
    exit 1
fi

# Display detected package manager
echo -e "${CYAN}Detected package manager: ${BOLD}${package_manager}${RESET}"

# Installing dependencies
echo -e "${YELLOW}[INFO] Checking and installing required system packages...${RESET}"
case $package_manager in
    "apt-get")
        sudo $package_manager update -y && sudo $package_manager install -y python3 python3-pip
        ;;
    "dnf" | "yum")
        sudo $package_manager install -y python3 python3-pip
        ;;
    "zypper")
        sudo $package_manager install -y python3 python3-pip
        ;;
    "pacman")
        sudo $package_manager -Syu --noconfirm python python-pip
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

echo -e "${GREEN}[SUCCESS] Required system packages checked/installed.${RESET}"

# Installing Python packages
REQUIRED_PYTHON_PACKAGES=(openai requests psutil notify2 rich smtplib)

for pkg in "${REQUIRED_PYTHON_PACKAGES[@]}"; do
    if ! python3 -c "import $pkg" &> /dev/null; then
        echo -e "${YELLOW}[INFO] Installing missing Python package: $pkg${RESET}"
        pip3 install $pkg
    else
        echo -e "${GREEN}[INFO] Python package already installed: $pkg${RESET}"
    fi
done

# Prompt user for required data
read -p "Enter your OpenAI API key: " api_key
export OPENAI_API_KEY=$api_key

read -p "Enter your Discord Webhook URL (optional, press enter to skip): " discord_webhook_url

echo -e "${YELLOW}[INFO] Writing configuration to config.json...${RESET}"
cat > config.json <<EOL
{
    "log_files": ["/var/log/syslog", "/var/log/auth.log"],
    "email_settings": {
        "from_email": "your-email@example.com",
        "admin_email": "admin@example.com",
        "smtp_server": "smtp.example.com"
    },
    "discord_webhook_url": "$discord_webhook_url"
}
EOL

echo -e "${GREEN}[SUCCESS] Configuration saved to config.json.${RESET}"

# Final message
echo -e "${GREEN}[SUCCESS] Setup completed successfully.${RESET}"
echo -e "${CYAN}[INFO] Launching gptADMIN.py in 3 seconds...${RESET}"
sleep 3

python3 gptADMIN.py

#!/bin/bash

GREEN="\e[32m"
RED="\e[31m"
YELLOW="\e[33m"
CYAN="\e[36m"
BOLD="\e[1m"
RESET="\e[0m"

divider() {
    echo -e "${CYAN}----------------------------------------------------${RESET}"
}

if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}${BOLD}[ERROR] You need to run this script as root.${RESET}"
    exit 1
fi

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

divider
echo -e "${CYAN}${BOLD}Detected package manager: ${package_manager}${RESET}"
divider

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
divider

REQUIRED_PYTHON_PACKAGES=(openai requests psutil notify2 rich smtplib backoff shlex notify2 json re subprocess plyer requests json)
echo -e "${YELLOW}[INFO] Checking and installing Python packages...${RESET}"
for pkg in "${REQUIRED_PYTHON_PACKAGES[@]}"; do
    if ! python3 -c "import $pkg" &> /dev/null; then
        echo -e "${YELLOW}[INSTALLING] ${pkg}...${RESET}"
        pip3 install $pkg
    else
        echo -e "${GREEN}[OK] ${pkg} is already installed.${RESET}"
    fi
done
echo -e "${GREEN}[SUCCESS] All Python packages are ready.${RESET}"
divider

echo -e "${CYAN}${BOLD}Configuration Setup${RESET}"
divider
read -p $' \e[36mEnter your OpenAI API key: \e[0m' api_key
export OPENAI_API_KEY=$api_key

read -p $' \e[36mEnter your Discord Webhook URL (optional, press enter to skip): \e[0m' discord_webhook_url

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
divider

echo -e "${GREEN}[SUCCESS] Setup completed successfully.${RESET}"
echo -e "${CYAN}[INFO] Launching gptADMIN.py in 3 seconds...${RESET}"
sleep 3

python3 gptADMIN.py

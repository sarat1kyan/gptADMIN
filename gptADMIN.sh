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
    echo -e "${RED}${BOLD}[ERROR] You need to run this script as root (use sudo).${RESET}"
    exit 1
fi

if ! command -v dos2unix &> /dev/null; then
    echo -e "${YELLOW}[INFO] Installing dos2unix...${RESET}"
    if [ -x "$(command -v apt-get)" ]; then
        sudo apt-get install -y dos2unix
    elif [ -x "$(command -v dnf)" ]; then
        sudo dnf install -y dos2unix
    elif [ -x "$(command -v yum)" ]; then
        sudo yum install -y dos2unix
    elif [ -x "$(command -v pacman)" ]; then
        sudo pacman -S --noconfirm dos2unix
    elif [ -x "$(command -v zypper)" ]; then
        sudo zypper install -y dos2unix
    else
        echo -e "${RED}[ERROR] Could not install dos2unix. Please install it manually.${RESET}"
        exit 1
    fi
fi

echo -e "${YELLOW}[INFO] Converting script to Unix format...${RESET}"
dos2unix "$0"

divider
echo -e "${CYAN}${BOLD}Setup Script - AI Log Monitor & Error Detection${RESET}"

divider
echo -e "${RED}${BOLD}[WARNING] Please read before continuing!${RESET}"
divider
echo -e "${YELLOW}"
echo "⚠️  This script integrates AI (OpenAI GPT) for log analysis and system monitoring."
echo "⚠️  AI-generated suggestions may be incorrect or unsafe. Use at your own risk!"
echo "⚠️  Ensure sensitive data (such as logs and API keys) is protected."
echo "⚠️  This tool does NOT replace professional system administration."
echo "⚠️  By proceeding, you acknowledge the risks and take full responsibility."
echo -e "${RESET}"
divider

read -p $' \e[36mDo you understand and agree to continue? (yes/no): \e[0m' user_agree
if [[ "$user_agree" != "yes" ]]; then
    echo -e "${RED}[ABORTED] Setup canceled by the user.${RESET}"
    exit 1
fi

divider
echo -e "${CYAN}${BOLD}Proceeding with setup...${RESET}"
divider

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
    echo -e "${RED}[ERROR] Unsupported package manager. Please install required packages manually.${RESET}"
    exit 1
fi

divider
echo -e "${CYAN}${BOLD}Detected package manager: ${package_manager}${RESET}"
divider

# Install required system packages
echo -e "${YELLOW}[INFO] Installing required system packages...${RESET}"
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

echo -e "${GREEN}[SUCCESS] Required system packages installed.${RESET}"
divider

REQUIRED_PYTHON_PACKAGES=(openai requests psutil rich smtplib backoff shlex plyer json re subprocess)
echo -e "${YELLOW}[INFO] Checking and installing Python packages...${RESET}"
for pkg in "${REQUIRED_PYTHON_PACKAGES[@]}"; do
    if ! python3 -c "import $pkg" &> /dev/null; then
        echo -e "${YELLOW}[INSTALLING] ${pkg}...${RESET}"
        pip3 install $pkg
    else
        echo -e "${GREEN}[OK] ${pkg} is already installed.${RESET}"
    fi
done
echo -e "${GREEN}[SUCCESS] All Python packages installed.${RESET}"
divider

echo -e "${CYAN}${BOLD}Configuration Setup${RESET}"
divider

while [[ -z "$api_key" ]]; do
    read -p $' \e[36mEnter your OpenAI API key: \e[0m' api_key
    if [[ -z "$api_key" ]]; then
        echo -e "${RED}[ERROR] OpenAI API Key cannot be empty!${RESET}"
    fi
done

echo "export OPENAI_API_KEY=$api_key" >> ~/.bashrc
source ~/.bashrc

read -p $' \e[36mEnter your Discord Webhook URL (optional, press enter to skip): \e[0m' discord_webhook_url

read -p $' \e[36mEnter your email (used for alerts): \e[0m' admin_email
read -p $' \e[36mEnter your SMTP server (e.g., smtp.gmail.com): \e[0m' smtp_server
read -p $' \e[36mEnter your SMTP port (e.g., 587 for TLS, 465 for SSL): \e[0m' smtp_port
read -p $' \e[36mUse TLS? (yes/no): \e[0m' use_tls

if [[ "$use_tls" == "yes" ]]; then
    use_tls_value=true
else
    use_tls_value=false
fi

echo -e "${YELLOW}[INFO] Writing configuration to config.json...${RESET}"
cat > config.json <<EOL
{
    "log_files": [
        "/var/log/syslog",
        "/var/log/auth.log",
        "/var/log/kern.log",
        "/var/log/faillog",
        "/var/log/cron.log",
        "/var/log/mail.log",
        "/var/log/mysqld.log",
        "/var/log/mariadb/mariadb.log",
        "/var/log/httpd/error_log",
        "/var/log/apache2/error.log",
        "/var/log/nginx/error.log",
        "/var/log/Xorg.0.log",
        "/var/log/messages",
        "/var/log/boot.log",
        "/var/log/yum.log",
        "/var/log/secure",
        "/var/log/journal",
        "/var/log/maillog",
        "/var/log/alternatives.log",
        "/var/log/btmp",
        "/var/log/wtmp",
        "/var/log/lastlog",
        "/var/log/sudo.log",
        "/var/log/apt/history.log",
        "/var/log/apt/term.log",
        "/var/log/audit/audit.log",
        "/var/log/lightdm/lightdm.log",
        "/var/log/Xorg.1.log",
        "/var/log/user.log"
    ],
    "email_settings": {
        "from_email": "$admin_email",
        "admin_email": "$admin_email",
        "smtp_server": "$smtp_server",
        "smtp_port": $smtp_port,
        "use_tls": $use_tls_value
    },
    "discord_webhook_url": "$discord_webhook_url"
}
EOL

echo -e "${GREEN}[SUCCESS] Configuration saved successfully.${RESET}"
echo -e "${YELLOW}[INFO] Please restart your terminal or run: source ~/.bashrc${RESET}"
divider

echo -e "${GREEN}[SUCCESS] Setup completed successfully.${RESET}"
echo -e "${CYAN}[INFO] Launching gptADMIN.py in 3 seconds...${RESET}"
sleep 3

python3 gptADMIN.py

███╗░░░███╗░█████╗░░█████╗░███╗░░██╗░⏾░██╗░░░░░██╗████████╗
████╗░████║██╔══██╗██╔══██╗████╗░██║░░░██║░░░░░██║╚══██╔══╝
██╔████╔██║██║░░██║██║░░██║██╔██╗██║░░░██║░░░░░██║░░░██║░░░
██║╚██╔╝██║██║░░██║██║░░██║██║╚████║░░░██║░░░░░██║░░░██║░░░
██║░╚═╝░██║╚█████╔╝╚█████╔╝██║░╚███║░░░███████╗██║░░░██║░░░
╚═╝░░░░░╚═╝░╚════╝░░╚════╝░╚═╝░░╚══╝░░░╚══════╝╚═╝░░░╚═╝░░░

# MoonLit 3.54 Stable Stable

# Sysadmin Assistant with ChatGPT 🛠️

Effortlessly streamline your Linux sysadmin tasks with the Sysadmin Assistant – a powerful tool that combines real-time error monitoring, interactive ChatGPT troubleshooting, and comprehensive system insights.

## 🚀 Key Features

- **Real-time Error Monitoring**: Keep an eye on system logs for errors as they happen.
- **Interactive ChatGPT Troubleshooting**: Engage in natural conversations with ChatGPT for expert solutions.
- **Comprehensive System Insights**: Display vital system information including distribution, kernel, CPU, RAM, and more.

## 📦 Installation

Get started quickly:

1. Clone this repository to your local machine.
2. Run the setup script to install necessary dependencies and configure your API key:
    ```bash
    chmod +x setup.sh
    bash setup.sh
    ```
3. The setup script will prompt you to enter your OpenAI API key. Make sure to have an OpenAI account and generate an API key.
4. The Alarming system has been added woth Update 3.54 Stable Stable so now you can get updates and alarms to your email or Discord channel using the webhook.
4.1 If you prefer use this tool without the alarming system just write NULL for email settings.
   
## 💡 Usage

1. Once setup is complete, run the main script using:
    ```bash
    python3 MoonLit.py
    ```
2. The script will proactively monitor system logs for errors.
3. When an error is detected, initiate a ChatGPT session for in-depth troubleshooting.
4. Now with Update 3.54 Stable Stable you also can perform system diagnostics
5. Exit the chat session by typing 'exit' or 'quit'.
6. Stop the Sysadmin Assistant with Ctrl+C.

## ⚠️ Caution

- Always exercise caution when using scripts with elevated privileges.
- Understand the implications of actions based on ChatGPT's advice.
- Review and validate responses before implementing changes on your system.

## 🌐 Supported Distributions

Installation script supports a range of popular package managers:
- apt-get (Debian/Ubuntu)
- dnf/yum (Fedora/RHEL/CentOS)
- zypper (openSUSE)
- pacman (Arch Linux)
- apk (Alpine Linux)
- eopkg (Solus)
- xbps-install (Void Linux)
- pisi (Pardus)
- swupd (Clear Linux)
- and more...

## ✨ Contribute

There may be and would be false positives or false negatives
so be careful and do not use this tool on production automation.
But this tool may help to decrease the time spent on production 

Feel free to contribute by creating pull requests or reporting issues.

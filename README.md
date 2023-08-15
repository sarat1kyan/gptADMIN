                                             
             _   _____ ____  _____ _____ _____ 
     ___ ___| |_|  _  |    \|     |     |   | |
    | . | . |  _|     |  |  | | | |-   -| | | |
    |_  |  _|_| |__|__|____/|_|_|_|_____|_|___|
    |___|_|                                    


# gptADMIN

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
    chmod +x gptADMIN.sh
    ./gptADMIN.sh
    ```
3. The setup script will prompt you to enter your OpenAI API key. Make sure to have an OpenAI account and generate an API key.

## 💡 Usage

1. Once setup is complete, run the main script using:
    ```bash
    python3 gptADMIN.py
    ```
2. The script will proactively monitor system logs for errors.
3. When an error is detected, initiate a ChatGPT session for in-depth troubleshooting.
4. Exit the chat session by typing 'exit' or 'quit'.
5. Stop the Sysadmin Assistant with Ctrl+C.

## ⚠️ Caution

- Always exercise caution when using scripts with elevated privileges.
- Understand the implications of actions based on ChatGPT's advice.
- Review and validate responses before implementing changes on your system.

## 🌐 Supported Distributions

Our installation script supports a range of popular package managers:
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

Feel free to contribute by creating pull requests or reporting issues.
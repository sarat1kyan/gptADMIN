                                __ _ _     _____  ___  
	  /\/\   ___   ___  _ __   / /(_) |_  |___ / / _ \ 
	 /    \ / _ \ / _ \| '_ \ / / | | __|   |_ \| | | |
	/ /\/\ \ (_) | (_) | | | / /__| | |_   ___) | |_| |
	\/    \/\___/ \___/|_| |_\____/_|\__| |____(_)___/ 
	                                                   
                                       
                                                  
                                                                                             
# MoonLit 3.82 Stable Stable

# Sysadmin Assistant with ChatGPT 🛠️

Effortlessly manage your Linux/MacOS/Windows sysadmin tasks with the AI - Powered Sysadmin Assistant – a powerful tool that combines real-time error monitoring, interactive ChatGPT troubleshooting, and comprehensive system insights.

	MacOS and Windows support coming soon (with Stable Version 4.1)

MoonLit - Advanced System Monitoring & Control

🌙 MoonLit is a powerful AI-integrated system monitoring, automation, and management tool. 
It allows system administrators to remotely control their servers via a Telegram bot, monitor system logs, receive error notifications, perform automated diagnostics, and execute system commands securely.

## 📌 **Features**

	✅ System Monitoring: Get real-time system performance, memory, disk, and network usage.
	✅ Log Analysis: Monitors system logs for errors and suggests fixes using AI (Stable release coming soon).
	✅ Automated Diagnostics: Provides detailed system health reports.
	✅ Remote Control via Telegram: Execute commands directly from Telegram.
	✅ Error Handling & Notifications: Sends alerts via email, Telegram, and desktop notifications.
	✅ Secure Execution: Allows admins to run system commands while ensuring security.
	✅ Automated System Updates: Fetch and install the latest updates for your server.
	✅ Discord Webhook Notifications: Send important logs and alerts to Discord.

## 🛠️ **Installation**

1️⃣ **Prerequisites**

Before running MoonLit, ensure you have:

	Linux-based system (Ubuntu, Debian, CentOS, Arch, etc.)
	Python 3.7+
	pip3 (Python package manager)
	Git
	A Telegram bot token (if using Telegram remote control)
	An OpenAI API key (optional, for AI-generated suggestions)
	SMTP credentials (if using email notifications)

2️⃣ **Install Required Packages**

Run the setup script to automatically install dependencies:

    
    sudo chmod +x setup.sh && sudo ./setup.sh
    

**This will:**	
	Install Python3, pip, and system dependencies
	Install required Python packages
	Configure Telegram, OpenAI, email, and Discord webhook settings

## ⚙️ **Manual Configuration**

All MoonLit configurations are save in 

	config.json

After installation, you can manually configure MoonLit by editing the config.json file if needed

💡 Ensure correct values before running the program!

## 🚀 **Running MoonLit**

To start MoonLit, run:
    
    python3 moonlit.py
    

## 🖥️ **Main Menu**

When running MoonLit, you’ll see a menu with the following options:

**Option	Description**
1	Monitor System Logs for Errors
2	Start Telegram Remote Control
3	View Error History
4	Check System Diagnostics
5	Adjust Settings
6	Check for Assistant Updates
7	Exit

📌 **Select an option by entering the corresponding number.**

📟 **Telegram Bot Usage**

If you’ve configured Telegram bot control, you can remotely manage your server via Telegram.

📝 Commands Available:

	/status → Check system uptime
	/services → List running services
	/disk → Show disk usage
	/memory → Show memory usage
	/network → Show network info
	/update → Update the system
	/restart → Restart the server
	/shutdown → Shutdown the server
	/exec <command> → Execute a custom Linux command
	/help → Show available commands
	/about → Display bot details

🔘 **Telegram Keyboard**

The bot provides an interactive keyboard for quick command access.

📊 System Diagnostics

MoonLit can automatically diagnose your system and report:

	✅ CPU Usage
	✅ Memory Usage
	✅ Disk Space
	✅ Running Services
	✅ Recent System Errors

To run diagnostics manually:

    
    python3 moonlit.py
    
    
Then choose option 4 (Check System Diagnostics).

## 📡 **Notifications**

💬 **MoonLit can send alerts to:**
	Telegram (via bot)
	Email (SMTP setup required)
	Desktop Notifications (for GUI-enabled servers)
	Discord Webhook (if enabled)

🔔 **Example notifications:**
	“High CPU Usage Detected!”
	“Service Failure: Apache2 stopped unexpectedly!”
	“Critical System Error: Kernel Panic”

## ⚡ **Updating MoonLit**

To update to the latest version:

    
    python3 moonlit.py
    

Select option 6 (Check for Assistant Updates).
Or manually update:

    
    git pull origin main
    

## 🛠️ **Troubleshooting**

	1️⃣ Telegram Bot Not Responding?
	Ensure your bot token is correct in config.json
	Check if the bot is running (python3 moonlit.py)
	Restart the bot:
 
    
    pkill -f "python3 moonlit.py"
    python3 moonlit.py
    

	2️⃣ **System Logs Not Being Monitored?**
	Ensure config.json has the correct log_files
	Run MoonLit with sudo (for full log access):

    
    python3 moonlit.py
    

	3️⃣ **OpenAI API Not Working?**
	Ensure you’ve set the OPENAI_API_KEY in config.json
	Check API quota at: OpenAI Account

## 👨‍💻 **Developers & Contributors**

🌍 Open Source Contribution: [GitHub Repo]([url](https://github.com/sarat1kyan/MoonLit))
📞 Support & Feedback: [Telegram]([url](https://t.me/saratikyan_m))
🛠️ Maintainer: Mher Saratikyan

## 📜 **License**

🔓 MoonLit is open-source software. You are free to modify and distribute it under the MIT License.

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

## 🚀 **Final Thoughts**

	🔹 MoonLit is your all-in-one Linux/MacOS/Windows assistant, combining AI-powered log analysis, system monitoring, and remote control.
	💡 Monitor, control, and secure your server with ease!
	🔧 Try it today and make Linux management easier!

## ✨ Contribute

There may be and would be false positives or false negatives
so be careful and do not use this tool on production automation.
But this tool may help to decrease the time spent on production 

Feel free to contribute by creating pull requests or reporting issues.

## **🚀 Happy Monitoring! 🌙**

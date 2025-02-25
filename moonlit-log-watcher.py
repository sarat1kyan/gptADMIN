import time
import os
import re
import logging
from moonlit import send_alert 

logging.basicConfig(
    filename="log_monitor.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

LOG_FILES = [
    # 🔹 System Logs
    "/var/log/syslog",
    "/var/log/messages",
    "/var/log/dmesg",
    "/var/log/kern.log",
    "/var/log/boot.log",
    "/var/log/alternatives.log",
    
    # 🔹 Authentication & Security Logs
    "/var/log/auth.log",
    "/var/log/secure",
    "/var/log/faillog",
    "/var/log/sudo.log",
    "/var/log/btmp",
    "/var/log/wtmp",
    "/var/log/lastlog",
    "/var/log/audit/audit.log",
    "/var/log/fail2ban.log",
    
    # 🔹 Package Management Logs
    "/var/log/dpkg.log",         # Debian/Ubuntu package manager
    "/var/log/yum.log",          # RHEL/CentOS package manager
    "/var/log/apt/history.log",
    "/var/log/apt/term.log",
    
    # 🔹 Web Server Logs
    "/var/log/nginx/access.log",
    "/var/log/nginx/error.log",
    "/var/log/httpd/access_log",
    "/var/log/httpd/error_log",
    "/var/log/apache2/access.log",
    "/var/log/apache2/error.log",
    
    # 🔹 Database Logs
    "/var/log/mysqld.log",
    "/var/log/mariadb/mariadb.log",
    "/var/log/postgresql/postgresql.log",
    "/var/log/mongodb/mongod.log",
    
    # 🔹 Email & Mail Server Logs
    "/var/log/mail.log",
    "/var/log/maillog",
    
    # 🔹 Job Scheduler & Cron Logs
    "/var/log/cron.log",
    "/var/log/cron",
    
    # 🔹 Firewall & Network Logs
    "/var/log/ufw.log",          # Uncomplicated Firewall (UFW)
    "/var/log/nftables.log",
    "/var/log/ipfirewall.log",
    
    # 🔹 Container & Virtualization Logs
    "/var/log/docker.log",
    "/var/log/kubelet.log",
    
    # 🔹 Xorg & Display Logs
    "/var/log/Xorg.0.log",
    "/var/log/Xorg.1.log",
    "/var/log/lightdm/lightdm.log",
    
    # 🔹 Miscellaneous Application Logs
    "/var/log/journal",          # Systemd Journal logs
    "/var/log/user.log",
    "/var/log/samba/log.smbd",   # Samba file sharing logs
    "/var/log/proftpd/proftpd.log", # FTP logs
    "/var/log/clamav/clamav.log" # ClamAV antivirus logs
]

ALERT_KEYWORDS = [
    "FAILED", "error", "segfault", "panic", "unauthorized", "denied",
    "disk full", "critical", "fatal", "attack", "malware", "rootkit",
    "intrusion", "brute force", "sql injection", "dos", "overload",
    "banned", "blocked", "timeout", "corrupt", "compromised", "root access",
    "firewall breach", "unusual login", "suspicious", "DDoS"
]

recent_alerts = {}

def send_unique_alert(message):
    global recent_alerts
    if message in recent_alerts:
        return  # Skip duplicate alert

    send_alert(message)  # Send Telegram alert
    recent_alerts[message] = time.time()

    for key in list(recent_alerts.keys()):
        if time.time() - recent_alerts[key] > 300:  # Keep for 5 mins
            del recent_alerts[key]

def tail_file(filename):
    try:
        with open(filename, "r") as file:
            file.seek(0, os.SEEK_END)  # Move to end of file
            while True:
                line = file.readline()
                if not line:
                    time.sleep(1)  # Wait for new lines
                    continue
                
                for keyword in ALERT_KEYWORDS:
                    if re.search(rf"\b{keyword}\b", line, re.IGNORECASE):
                        logging.warning(f"ALERT TRIGGERED: {line.strip()}")
                        send_unique_alert(line.strip())  # Send alert
                        break
    except Exception as e:
        logging.error(f"Failed to read {filename}: {e}")

if __name__ == "__main__":
    logging.info("🔍 Log monitoring started...")

    for log_file in LOG_FILES:
        if os.path.exists(log_file):
            logging.info(f"Monitoring {log_file} for alerts...")
            tail_file(log_file)
        else:
            logging.warning(f"⚠️ Log file not found: {log_file}")

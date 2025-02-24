import os
import re
import time
import subprocess
import openai
import logging
import json
import smtplib
import psutil
import telebot
import threading
from datetime import datetime
from plyer import notification
import shlex
import platform
import requests
import backoff
from rich.console import Console
from rich.table import Table
from rich.progress import track
from rich.prompt import Prompt
from rich.panel import Panel
from rich.text import Text
from email.mime.text import MIMEText
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.types import ReplyKeyboardMarkup, KeyboardButton


console = Console()
RESTRICTED_COMMANDS = ["rm -rf /", "shutdown -h now", "passwd", "dd if=/dev/zero of=/dev/sda", "mkfs.ext4", "chmod 777"]
logging.basicConfig(filename='assistant.log', level=logging.INFO)
logging.basicConfig(filename='error_log.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
client = openai.OpenAI() 
openai.api_key = os.getenv("OPENAI_API_KEY")
with open('config.json') as f:
    config = json.load(f)

TELEGRAM_BOT_TOKEN = config["telegram_bot_token"]
TELEGRAM_ADMIN_ID = str(config["telegram_admin_id"])
LOG_FILE = "/var/log/MoonLit_commands.log"

ALLOWED_COMMANDS = ["status", "restart", "update", "shutdown", "services", "disk", "memory", "network", "exec"]

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

def execute_command(command):
    try:
        logging.info(f"Executing command: {command}")

        if command == "status":
            output = subprocess.run("uptime", shell=True, capture_output=True, text=True)
        elif command == "restart":
            output = subprocess.run("sudo reboot", shell=True, capture_output=True, text=True)
            return "🔄 System is restarting..."
        elif command == "update":
            output = subprocess.run("sudo apt update && sudo apt upgrade -y", shell=True, capture_output=True, text=True)
        elif command == "shutdown":
            output = subprocess.run("sudo shutdown -h now", shell=True, capture_output=True, text=True)
            return "⚠️ System is shutting down..."
        elif command == "services":
            output = subprocess.run("systemctl list-units --type=service --state=running", shell=True, capture_output=True, text=True)
        elif command == "disk":
            output = subprocess.run("df -h", shell=True, capture_output=True, text=True)
        elif command == "memory":
            output = subprocess.run("free -m", shell=True, capture_output=True, text=True)
        elif command == "network":
            output = subprocess.run("ip a", shell=True, capture_output=True, text=True)
        else:
            return "❌ Unknown command."

        return f"✅ Command executed:\n```{output.stdout[:1900]}```"  # Telegram messages max 2000 chars

    except Exception as e:
        logging.error(f"Error executing {command}: {e}")
        return f"❌ Error executing {command}: {e}"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    """Sends a welcome message with a persistent keyboard."""
    logging.debug(f"Received /start from {message.chat.id}")

    if str(message.chat.id) != TELEGRAM_ADMIN_ID:
        bot.reply_to(message, "🚫 *You are not authorized to use this bot.*", parse_mode="MarkdownV2")
        return

    welcome_text = (
        "🌙 *Welcome to MoonLit Admin Bot\* \n\n"
        "🔧 *Your personal system administrator in Telegram\* 🚀\n"
        "💡 *Control your server securely from anywhere\\.*\n\n"
        "📌 *Features:* \n"
        "✅ System Monitoring \n"
        "✅ Server Control \n"
        "✅ Log Checking \n"
        "✅ Custom Command Execution \n\n"
        "Use the buttons below or type /help for more commands"
    )

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    keyboard.add(
        KeyboardButton("📊 Check Status"),
        KeyboardButton("📜 List Services")
    )
    keyboard.add(
        KeyboardButton("💾 Disk Usage"),
        KeyboardButton("🧠 Memory Usage")
    )
    keyboard.add(
        KeyboardButton("🌐 Network Info"),
        KeyboardButton("🔄 Update System")
    )
    keyboard.add(
        KeyboardButton("⚠️ Restart"),
        KeyboardButton("🔴 Shutdown")
    )
    keyboard.add(KeyboardButton("ℹ️ Help"), KeyboardButton("❓ About")) 

    bot.send_message(message.chat.id, welcome_text, reply_markup=keyboard, parse_mode="MarkdownV2")
    
@bot.message_handler(commands=['help'])

@bot.message_handler(commands=['about'])
def send_about(message):
    logging.debug(f"Received /about from {message.chat.id}")

    if str(message.chat.id) != TELEGRAM_ADMIN_ID:
        bot.reply_to(message, "🚫 *You are not authorized to use this bot.*", parse_mode="MarkdownV2")
        return

    about_text = (
        "❓ *About MoonLit Bot*\n\n"
        "🌙 *MoonLit is a powerful Telegram bot designed for system monitoring and management* \n"
        "🔧 It provides easy access to system commands, logs, and performance data\.\n"
        "🛡️ Secure, reliable, and easy to use\.\n\n"
        "💡 *Developed for system admins who want full control over their servers remotely* 🚀\n\n"
        "📌 *Main Features:* \n"
        "• 📊 System Monitoring\n"
        "• 🖥️ Server Control\n"
        "• 📜 Log Analysis\n"
        "• ⚡ Quick Access to Linux Commands\n\n"
        "🔗 *Project Maintainer:* `Mher Saratikyan`\n"
        "🌍 *Open Source Contribution:* [GitHub Repo](https://github.com/sarat1kyan/MoonLit)\n"
        "📞 *Support:* [Telegram Group](https://t.me/saratikyan_m)"
    )

    bot.send_message(message.chat.id, about_text, parse_mode="MarkdownV2", disable_web_page_preview=True)
    
@bot.message_handler(commands=['help'])
def send_help(message):
    logging.debug(f"Received /help from {message.chat.id}")

    if str(message.chat.id) != TELEGRAM_ADMIN_ID:
        bot.reply_to(message, "🚫 *You are not authorized to use this bot.*", parse_mode="MarkdownV2")
        return

    help_text = (
        "ℹ️ *MoonLit Bot Commands*\n\n"
        "📌 *System Monitoring Commands:*\n"
        "• `/status` – Check system uptime 🕒\n"
        "• `/services` – List running services 📜\n"
        "• `/disk` – Show disk usage 💾\n"
        "• `/memory` – Show memory usage 🧠\n"
        "• `/network` – Show network info 🌐\n\n"
        "⚙️ *System Control Commands:*\n"
        "• `/update` – Update the system 🔄\n"
        "• `/restart` – Restart the server ⚠️\n"
        "• `/shutdown` – Shutdown the server 🔴\n\n"
        "🛠 *Custom Execution:*\n"
        "• `/exec <command>` – Run any Linux command ⚡\n\n"
        "❓ *Other Commands:*\n"
        "• `/help` – Show this help message ℹ️\n"
        "• `/about` – About the bot ❓\n\n"
        "💡 *Use the buttons below or type a command*"
    )

    bot.send_message(message.chat.id, help_text, parse_mode="MarkdownV2")


@bot.message_handler(func=lambda message: True)
def handle_keyboard_buttons(message):
    user_id = str(message.chat.id)

    if user_id != TELEGRAM_ADMIN_ID:
        bot.reply_to(message, "🚫 *You are not authorized to use this bot.*", parse_mode="MarkdownV2")
        return

    command_map = {
        "📊 Check Status": "status",
        "📜 List Services": "services",
        "💾 Disk Usage": "disk",
        "🧠 Memory Usage": "memory",
        "🌐 Network Info": "network",
        "🔄 Update System": "update",
        "⚠️ Restart": "restart",
        "🔴 Shutdown": "shutdown",
        "ℹ️ Help": "help",
        "❓ About": "about"
    }

    command = command_map.get(message.text)

    if command == "help":
        send_help(message)  # Call help function
    elif command == "about":
        send_about(message)  # Call about function
    elif command in ["status", "restart", "update", "shutdown", "services", "disk", "memory", "network"]:
        response = execute_command(command)
        bot.send_message(message.chat.id, response, parse_mode="MarkdownV2")
    else:
        bot.reply_to(message, escape_markdown_v2("❌ Invalid command. Use the buttons below or /help."), parse_mode="MarkdownV2")
        
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    user_id = str(call.message.chat.id)

    if user_id != TELEGRAM_ADMIN_ID:
        bot.answer_callback_query(call.id, "🚫 You are not authorized!")
        return

    command = call.data
    response = execute_command(command)
    bot.send_message(call.message.chat.id, response)

def escape_markdown_v2(text):
    return re.sub(r'([_*\[\]()~`>#+-=|{}.!])', r'\\\1', text)

@bot.message_handler(commands=['exec'])
def execute_custom_command(message):
    user_id = str(message.chat.id)

    if user_id != TELEGRAM_ADMIN_ID:
        bot.reply_to(message, "🚫 *You are not authorized to run this command.*", parse_mode="MarkdownV2")
        return

    command = message.text.replace("/exec", "").strip()

    if not command:
        bot.reply_to(message, "❌ *Please provide a command to execute.*\nExample:\n`/exec ls -lah`", parse_mode="MarkdownV2")
        return

    # Prevent execution of dangerous commands
    for restricted in RESTRICTED_COMMANDS:
        if restricted in command:
            bot.reply_to(message, f"⚠️ *Command is blocked for security reasons:* `{restricted}`", parse_mode="MarkdownV2")
            return

    # Confirm execution before proceeding
    confirm_keyboard = InlineKeyboardMarkup()
    confirm_keyboard.add(
        InlineKeyboardButton("✅ Run", callback_data=f"exec_run:{command}"),
        InlineKeyboardButton("❌ Cancel", callback_data="exec_cancel")
    )

    bot.send_message(message.chat.id, f"⚠️ *Confirm Execution:* `{escape_markdown_v2(command)}`", 
                     parse_mode="MarkdownV2", reply_markup=confirm_keyboard)

@bot.callback_query_handler(func=lambda call: call.data.startswith("exec_run:") or call.data == "exec_cancel")
def confirm_execution(call):
    """Handles the execution confirmation buttons."""
    user_id = str(call.message.chat.id)

    if user_id != TELEGRAM_ADMIN_ID:
        bot.answer_callback_query(call.id, "🚫 You are not authorized!")
        return

    if call.data == "exec_cancel":
        bot.answer_callback_query(call.id, "❌ Command execution canceled.")
        bot.edit_message_text("❌ *Execution Canceled.*", chat_id=call.message.chat.id, 
                              message_id=call.message.message_id, parse_mode="MarkdownV2")
        return

    command = call.data.replace("exec_run:", "")

    bot.answer_callback_query(call.id, "✅ Running command...")

    try:
        start_time = time.time()
        output = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=10)
        duration = time.time() - start_time

        result = output.stdout if output.stdout else output.stderr
        escaped_result = escape_markdown_v2(result)

        response_message = f"✅ *Command Executed in {duration:.2f}s:*\n```\n{escaped_result[:1900]}\n```"

        if len(escaped_result) > 1900:  # If output is too long, send as a file
            log_filename = f"command_output_{int(time.time())}.txt"
            with open(log_filename, "w") as log_file:
                log_file.write(result)
            with open(log_filename, "rb") as log_file:
                bot.send_document(call.message.chat.id, log_file, caption="📄 Full command output")
            os.remove(log_filename)
        else:
            bot.send_message(call.message.chat.id, response_message, parse_mode="MarkdownV2")

    except subprocess.TimeoutExpired:
        bot.send_message(call.message.chat.id, "❌ *Command timed out after 10 seconds.*", parse_mode="MarkdownV2")
    except Exception as e:
        bot.send_message(call.message.chat.id, f"❌ *Error executing command:* `{escape_markdown_v2(str(e))}`", parse_mode="MarkdownV2")

    bot.edit_message_text(f"✅ *Command Executed:* `{escape_markdown_v2(command)}`", 
                          chat_id=call.message.chat.id, message_id=call.message.message_id, parse_mode="MarkdownV2")

        
def start_telegram_bot():
    """Starts the Telegram bot in a separate thread when the user selects it."""
    console.print("[green]✅ Telegram bot is now running! Send commands in Telegram.[/green]")
    bot.polling(none_stop=True)

logging.debug("Starting Telegram bot...")

def is_headless():
    return not os.getenv("DISPLAY") and not os.getenv("DBUS_SESSION_BUS_ADDRESS")

if is_headless():
    console.print("[yellow]Skipping notify2: No GUI detected (headless mode).[/yellow]")
else:
    try:
        notify2.init("AI Assistant")
    except Exception as e:
        console.print(f"[red]Functionality check completed[/red]")

if not openai.api_key:
    console.print("[red]OpenAI API key not found. Please set it in environment variables.[/red]")
    exit(1)

log_files = config['log_files']
email_settings = config['email_settings']

if not openai.api_key:
    console.print("[red]OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.[/red]")
    raise ValueError("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")

import requests
import json

@bot.message_handler(func=lambda message: message.text.startswith('/'))
def handle_command(message):
    """Handles predefined system commands."""
    user_id = str(message.chat.id)

    if user_id != TELEGRAM_ADMIN_ID:
        bot.reply_to(message, "🚫 You are not authorized to run this command.")
        return

    command = message.text.lstrip("/")

    if command in ALLOWED_COMMANDS:
        response = execute_command(command)
        bot.reply_to(message, response)
    else:
        bot.reply_to(message, "❌ Invalid command. Use /help for available commands.")

def send_discord_notification(title, message):

    try:
        with open("config.json", "r") as f:
            config = json.load(f)

        webhook_url = config.get("discord_webhook_url")
        if not webhook_url:
            print("[ERROR] No Discord webhook URL found in config.json")
            return

        payload = {
            "username": "MoonLit",
            "embeds": [
                {
                    "title": title,
                    "description": message,
                    "color": 5814783, 
                    "footer": {"text": "Sent by MoonLit"}
                }
            ]
        }

        response = requests.post(webhook_url, json=payload)

        if response.status_code == 204:
            print("[SUCCESS] Message sent to Discord successfully!")
        else:
            print(f"[ERROR] Failed to send message to Discord. Response: {response.status_code} - {response.text}")

    except Exception as e:
        print(f"[ERROR] Discord notification failed: {e}")

def display_menu():
    console.print(Panel("[bold cyan]AI Assistant - Main Menu[/bold cyan]", expand=False))
    table = Table(title="Main Menu", show_lines=True)
    table.add_column("Option", justify="center", style="cyan")
    table.add_column("Description", justify="left")
    table.add_row("1", "Monitor System Logs for Errors")
    table.add_row("2", "Start Telegram Remote Control")
    table.add_row("3", "View Error History")
    table.add_row("4", "Check System Diagnostics")
    table.add_row("5", "Adjust Settings")
    table.add_row("6", "Check for Assistant Updates")
    table.add_row("7", "Exit")

    console.print(table)

    choice = Prompt.ask("Select an option", choices=["1", "2", "3", "4", "5", "6", "7"], default="7")
    return choice

def monitor_logs():
    console.print(Panel("AI Assistant is monitoring the system...", title="AI Assistant"))
    try:
        while True:
            logs = get_journalctl_logs() 

            error_pattern = re.compile(r'(.*error.*)', re.IGNORECASE)
            matches = error_pattern.findall(logs)
            for error in matches:
                classify_and_handle_error(error, "journalctl")

            time.sleep(60)
    except KeyboardInterrupt:
        console.print("[bold red]Stopping AI Assistant.[/bold red]")

def classify_and_handle_error(error_message, source):
    if "critical" in error_message.lower() or "fail" in error_message.lower():
        severity = "critical"
        severity_style = "[bold red]"
    elif "warning" in error_message.lower():
        severity = "warning"
        severity_style = "[bold yellow]"
    else:
        severity = "info"
        severity_style = "[bold green]"
    logging.info(f"{severity.capitalize()} Error Detected in {source}: {error_message}")

    console.print(f"[{severity_style}]{severity.capitalize()} Error Detected in {source}: {error_message}[/]")
    send_desktop_notification(severity, error_message)
    explain_and_suggest_fix(error_message, severity)

def send_desktop_notification(severity, message):
    if os.getenv("DISPLAY"): 
        notification.notify(
            title=f"{severity.capitalize()} Error Detected",
            message=message,
            app_name="AI Assistant"
        )
    else:
        try:
            subprocess.run(["notify-send", f"{severity.capitalize()} Error", message])
        except FileNotFoundError:
            print(f"Notification failed: No GUI or notify-send available.")
            
def get_journalctl_logs():
    try:
        result = subprocess.run(
            ["journalctl", "-n", "100", "--no-pager"],  # Get last 100 lines
            text=True,
            capture_output=True
        )
        return result.stdout
    except Exception as e:
        return f"Error retrieving logs: {e}"

def get_gpt_response(conversation):
    return openai.ChatCompletion.create(
        model="gpt-4o-2024-08-06",
        messages=conversation,
        timeout=10
    )
'''
def explain_and_suggest_fix(error_message, severity):
    console.print(f"[cyan]Analyzing {severity} error with GPT...[/cyan]")

    system_info = f"OS: {os.uname().sysname} {os.uname().release}, Python: {platform.python_version()}"
    conversation = [
    {"role": "system", "content": "You are a sysadmin assistant. Help the user troubleshoot system errors."},
    {"role": "user", "content": f"System Info: {system_info}. Error: {error_message}. Please provide an explanation and suggest shell commands to fix it."}
]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-2024-08-06",
            messages=conversation,
            timeout=10  
        )
        suggestion = response['choices'][0]['message']['content']
        console.print(Panel(suggestion, title="GPT Explanation & Suggested Fix"))

        suggested_commands = extract_commands_from_gpt(suggestion)

        if suggested_commands:
            console.print(f"[yellow]Suggested commands to execute:[/yellow] {suggested_commands}")
        else:
            console.print("[yellow]No shell commands provided by GPT. Manual intervention may be required.[/yellow]")
        
        user_choice = Prompt.ask("Do you want me to try these commands?", choices=["yes", "no"], default="no")
        if user_choice == "yes" and suggested_commands:
            perform_fix(suggested_commands)
        else:
            console.print("[yellow]No fix will be applied.[/yellow]")
    
    except Exception as e:
        console.print(f"[red]Error in GPT request: {e}[/red]")
        logging.error(f"GPT request error: {e}")
'''
'''
def explain_and_suggest_fix(error_message, severity):
    print(f"[INFO] Analyzing {severity} error with GPT...")

    system_info = f"OS: {os.uname().sysname} {os.uname().release}, Python: {platform.python_version()}"
    conversation = [
        {"role": "system", "content": "You are a sysadmin assistant. Help troubleshoot system errors."},
        {"role": "user", "content": f"System Info: {system_info}. Error: {error_message}. Suggest a fix."}
    ]

    try:
        response = client.chat.completions.create(  
            model="gpt-4o-2024-08-06",
            messages=conversation
        )
        suggestion = response.choices[0].message.content  
        print(f"[GPT Suggestion] {suggestion}")

    except Exception as e:
        print(f"[ERROR] GPT request failed: {e}")
'''

def explain_and_suggest_fix(error_message, severity):
    print(f"[INFO] Analyzing {severity} error with GPT...")

    system_info = "Linux Server, Debian OS"
    conversation = [
        {"role": "system", "content": "You are a sysadmin assistant. Help troubleshoot system errors."},
        {"role": "user", "content": f"System Info: {system_info}. Error: {error_message}. Suggest a fix."}
    ]

    max_retries = 5  
    for attempt in range(max_retries):
        try:
            # First, try GPT-4
            try:
                response = client.chat.completions.create(
                    model="gpt-4o-2024-08-06",
                    messages=conversation
                )
            except openai.APIError as e:
                if "model_not_found" in str(e):
                    print("[WARNING] GPT-4 is unavailable. Falling back to GPT-3.5.")
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=conversation
                    )
                else:
                    raise e 

            suggestion = response.choices[0].message.content
            print(f"[GPT Suggestion] {suggestion}")
            return suggestion 

        except openai.APIError as e:
            if "insufficient_quota" in str(e):
                print("[ERROR] OpenAI quota exceeded! Check billing at https://platform.openai.com/account/billing")
                return
            elif attempt < max_retries - 1:
                wait_time = (2 ** attempt) + random.uniform(0, 1)
                print(f"[WARNING] OpenAI API request failed ({e}). Retrying in {wait_time:.2f} seconds...")
                time.sleep(wait_time)
            else:
                print("[ERROR] Failed after multiple retries.")
                return

def extract_commands_from_gpt(gpt_response):
    command_block_pattern = re.findall(r"```(?:bash|shell)?\n(.*?)\n```", gpt_response, re.DOTALL)

    extracted_commands = []
    for block in command_block_pattern:
        for line in block.splitlines():
            line = line.strip()
            if line and not line.startswith("#"):  
                line = line.lstrip("$ ")  
                extracted_commands.append(line)

    if not extracted_commands:
        command_pattern = re.compile(r"^\s*[\$#]?\s*(sudo|apt-get|systemctl|service|chmod|chown|rm|cp|mv|reboot|shutdown|df|ps|kill|netstat|ping|ifconfig|ls|grep|awk|sed|curl|wget|find).*", re.MULTILINE)
        extracted_commands = command_pattern.findall(gpt_response)

    return extracted_commands

def perform_fix(commands):
    try:
        for command in track(commands, description="Applying Fixes...", total=len(commands)):
            confirm = Prompt.ask(f"Execute this command? [bold]{command}[/bold]", choices=["yes", "no"], default="no")
            if confirm == "yes":
                safe_execute(command)
            else:
                console.print(f"[yellow]Skipped:[/yellow] {command}")
        console.print("[green]Fix process completed.[/green]")
    except Exception as e:
        console.print(f"[red]Failed to apply fix: {e}[/red]")
        logging.error(f"Error applying fix: {e}")

def safe_execute(command):
    try:
        console.print(f"[yellow]Running:[/yellow] {command}")
        result = subprocess.run(shlex.split(command), text=True, capture_output=True)
        if result.stdout:
            console.print(result.stdout)
        if result.stderr:
            console.print(f"[red]Error Output:[/red] {result.stderr}")
    except Exception as e:
        console.print(f"[red]Execution failed: {e}[/red]")

def log_fix(error_message, fix_details):
    log_entry = {
        "error": error_message,
        "fix": fix_details,
        "timestamp": time.ctime()
    }
    with open("fix_log.json", "a") as logfile:
        json.dump(log_entry, logfile)
        logfile.write("\n")

def show_history():
    try:
        with open("fix_log.json", "r") as logfile:
            for line in logfile:
                log_entry = json.loads(line)
                console.print(f"Error: {log_entry['error']}\nFix: {log_entry['fix']}\nTime: {log_entry['timestamp']}\n")
    except FileNotFoundError:
        console.print("[yellow]No historical logs found.[/yellow]")

def send_email_notification(subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = email_settings['from_email']
    msg['To'] = email_settings['admin_email']

    s = smtplib.SMTP(email_settings['smtp_server'])
    s.sendmail(msg['From'], [msg['To']], msg.as_string())
    s.quit()

def gather_diagnostics():
    console.print("[cyan][INFO] Running System Diagnostics...[/cyan]")

    uname = platform.uname()
    uptime = subprocess.run("uptime -p", shell=True, capture_output=True, text=True).stdout.strip()
    
    system_info = f"""
    **📌 System Info**
    🔹 OS: {uname.system} {uname.release} ({uname.version})  
    🔹 Hostname: {uname.node}  
    🔹 Uptime: {uptime}  
    """

    console.print(system_info)

    cpu_usage = psutil.cpu_percent(interval=1)
    cpu_freq = psutil.cpu_freq()
    load_avg = os.getloadavg() if hasattr(os, 'getloadavg') else (0, 0, 0)

    cpu_info = f"""
    **🖥️ CPU Info**
    🔹 CPU Usage: {cpu_usage}%  
    🔹 CPU Frequency: {cpu_freq.current:.2f} MHz  
    🔹 Load Average (1m, 5m, 15m): {load_avg}  
    """
    
    console.print(cpu_info)

    mem = psutil.virtual_memory()
    swap = psutil.swap_memory()

    memory_info = f"""
    **🧠 Memory Info**
    🔹 Total Memory: {mem.total / (1024 ** 3):.2f} GB  
    🔹 Used Memory: {mem.used / (1024 ** 3):.2f} GB ({mem.percent}%)  
    🔹 Swap Usage: {swap.used / (1024 ** 3):.2f} GB ({swap.percent}%)  
    """
    
    console.print(memory_info)

    disk = psutil.disk_usage('/')
    io_counters = psutil.disk_io_counters()

    disk_info = f"""
    **💾 Disk Info**
    🔹 Total Disk Space: {disk.total / (1024 ** 3):.2f} GB  
    🔹 Used Disk Space: {disk.used / (1024 ** 3):.2f} GB ({disk.percent}%)  
    🔹 Disk Reads: {io_counters.read_count} | Writes: {io_counters.write_count}  
    """
    
    console.print(disk_info)

    net_io = psutil.net_io_counters()
    net_errors = subprocess.run("dmesg | grep -i 'eth0\|wlan\|network'", shell=True, capture_output=True, text=True).stdout.strip()

    network_info = f"""
    **🌐 Network Info**
    🔹 Data Sent: {net_io.bytes_sent / (1024 ** 2):.2f} MB  
    🔹 Data Received: {net_io.bytes_recv / (1024 ** 2):.2f} MB  
    """

    if net_errors:
        network_info += f"\n⚠️ **Network Errors Detected:** {net_errors}"
    
    console.print(network_info)

    services = ["ssh", "apache2", "nginx", "mysql", "docker"]
    active_services = []
    
    for service in services:
        status = subprocess.run(f"systemctl is-active {service}", shell=True, capture_output=True, text=True).stdout.strip()
        if status == "active":
            active_services.append(service)

    services_info = f"""
    **🛠️ Running Services**
    {', '.join(active_services) if active_services else '[None]'}  
    """
    
    console.print(services_info)

    logs = subprocess.run("journalctl -p 3 -n 10 --no-pager", shell=True, capture_output=True, text=True).stdout.strip()

    logs_info = f"""
    **🔥 Recent System Errors**
    {logs if logs else "✅ No recent critical errors found."}  
    """

    console.print(logs_info)

    summary = f"""
    ✅ **Diagnostics completed successfully!**
    """

    console.print(summary)

    # **Send diagnostics to Discord**
    full_report = f"{system_info}\n{cpu_info}\n{memory_info}\n{disk_info}\n{network_info}\n{services_info}\n{logs_info}\n{summary}"
    send_discord_notification("📊 System Diagnostics Report", full_report)
def check_for_updates():
    console.print("[yellow][INFO] Checking for updates...[/yellow]")

    status_result = subprocess.run("git status --porcelain", shell=True, capture_output=True, text=True)
    if status_result.stdout.strip():
        console.print("[red][WARNING] You have uncommitted changes![/red]")

        user_choice = input("Do you want to (c)ommit, (s)tash, or (a)bort update? [c/s/a]: ").strip().lower()

        if user_choice == "c":
            commit_message = input("Enter commit message: ").strip()
            subprocess.run(f"git add . && git commit -m '{commit_message}'", shell=True)
        elif user_choice == "s":
            subprocess.run("git stash", shell=True)
            console.print("[yellow][INFO] Changes stashed temporarily.[/yellow]")
        elif user_choice == "a":
            console.print("[red][INFO] Update aborted.[/red]")
            return
        else:
            console.print("[red][ERROR] Invalid choice. Update aborted.[/red]")
            return

    console.print("[yellow]Applying updates...[/yellow]")
    for _ in track(range(10), description="Updating repository..."):
        subprocess.run("sleep 0.1", shell=True)

    update_result = subprocess.run("git pull origin main", shell=True, capture_output=True, text=True)

    if "Aborting" in update_result.stderr:
        console.print("[red][ERROR] Update failed! Resolve conflicts manually.[/red]")
        return

    console.print("[green][SUCCESS] Update applied successfully![/green]")

    stash_list = subprocess.run("git stash list", shell=True, capture_output=True, text=True).stdout
    if "stash@{0}" in stash_list:
        console.print("[yellow][INFO] Restoring stashed changes...[/yellow]")
        subprocess.run("git stash pop", shell=True)

    console.print("[green]Update process completed![/green]")
    
if __name__ == "__main__":
    while True:
        choice = display_menu()

        if choice == "1":
            monitor_logs()
            console.print("[yellow]Feature coming soon.[/yellow]")
        elif choice == "2":
            telegram_thread = threading.Thread(target=start_telegram_bot)
            telegram_thread.start()
            console.print("[yellow]Controll your server via Telegram[/yellow]")
        elif choice == "3":
            console.print("[yellow]View Error History[/yellow]")
            show_history()
        elif choice == "4":
            gather_diagnostics()
        elif choice == "5":
            console.print("[yellow]Settings can be changed also from config.json[/yellow]")
        elif choice == "6":
            check_for_updates()
        elif choice == "7":
            console.print("[green]Exiting AI Assistant.[/green]")
            break

import os
import re
import time
import subprocess
import openai
import logging
import json
import smtplib
import psutil
#import notify2
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

console = Console()

#if os.getenv("DISPLAY") or os.getenv("DBUS_SESSION_BUS_ADDRESS"):
#    notify2.init("AI Assistant")
#else:
#    console.print("[yellow]Skipping notify2: No GUI detected (headless mode).[/yellow]")
#
logging.basicConfig(filename='assistant.log', level=logging.INFO)
logging.basicConfig(filename='error_log.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
client = openai.OpenAI() 
openai.api_key = os.getenv("OPENAI_API_KEY")
with open('config.json') as f:
    config = json.load(f)

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

def send_discord_notification(message):
    webhook_url = "YOUR_DISCORD_WEBHOOK_URL"
    payload = {"content": message}
    requests.post(webhook_url, json=payload)

def display_menu():
    console.print(Panel("[bold cyan]AI Assistant - Main Menu[/bold cyan]", expand=False))
    table = Table(title="Main Menu", show_lines=True)
    table.add_column("Option", justify="center", style="cyan")
    table.add_column("Description", justify="left")
    table.add_row("1", "Monitor System Logs for Errors")
    table.add_row("2", "View Error History")
    table.add_row("3", "Check System Diagnostics")
    table.add_row("4", "Adjust Settings")
    table.add_row("5", "Check for Assistant Updates")
    table.add_row("6", "Exit")

    console.print(table)

    choice = Prompt.ask("Select an option", choices=["1", "2", "3", "4", "5", "6"], default="1")
    return choice

#def monitor_logs():
#    console.print(Panel("AI Assistant is monitoring the system...", title="AI Assistant"))
#    try:
#        while True:
#            for log_file in log_files:
#                try:
#                    with open(log_file, 'r') as f:
#                        logs = f.readlines()
#
#                    error_pattern = re.compile(r'(.*error.*)', re.IGNORECASE)
#                    matches = error_pattern.findall("".join(logs))
#                    for error in matches:
#                        classify_and_handle_error(error, log_file)
#                except FileNotFoundError:
#                    console.print(f"[yellow]Warning: {log_file} not found.[/yellow]")
#
#            time.sleep(60)
#    except KeyboardInterrupt:
#        console.print("[bold red]Stopping AI Assistant.[/bold red]")

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
            
#        n = notify2.Notification("Critical Error Detected", message, "dialog-warning")
#        n.set_urgency(notify2.URGENCY_CRITICAL)
#        n.show()

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
    
    console.print(f"\n[bold]📌 System Info:[/bold]")
    console.print(f"🔹 OS: {uname.system} {uname.release} ({uname.version})")
    console.print(f"🔹 Hostname: {uname.node}")
    console.print(f"🔹 Uptime: {uptime}")

    cpu_usage = psutil.cpu_percent(interval=1)
    cpu_freq = psutil.cpu_freq()
    load_avg = os.getloadavg() if hasattr(os, 'getloadavg') else (0, 0, 0)
    
    console.print(f"\n[bold]🖥️ CPU Info:[/bold]")
    console.print(f"🔹 CPU Usage: {cpu_usage}%")
    console.print(f"🔹 CPU Frequency: {cpu_freq.current:.2f} MHz")
    console.print(f"🔹 Load Average (1m, 5m, 15m): {load_avg}")

    mem = psutil.virtual_memory()
    swap = psutil.swap_memory()
    
    console.print(f"\n[bold]🧠 Memory Info:[/bold]")
    console.print(f"🔹 Total Memory: {mem.total / (1024 ** 3):.2f} GB")
    console.print(f"🔹 Used Memory: {mem.used / (1024 ** 3):.2f} GB ({mem.percent}%)")
    console.print(f"🔹 Swap Usage: {swap.used / (1024 ** 3):.2f} GB ({swap.percent}%)")

    disk = psutil.disk_usage('/')
    io_counters = psutil.disk_io_counters()
    
    console.print(f"\n[bold]💾 Disk Info:[/bold]")
    console.print(f"🔹 Total Disk Space: {disk.total / (1024 ** 3):.2f} GB")
    console.print(f"🔹 Used Disk Space: {disk.used / (1024 ** 3):.2f} GB ({disk.percent}%)")
    console.print(f"🔹 Disk Reads: {io_counters.read_count} | Writes: {io_counters.write_count}")

    net_io = psutil.net_io_counters()
    net_errors = subprocess.run("dmesg | grep -i 'eth0\|wlan\|network'", shell=True, capture_output=True, text=True).stdout.strip()
    
    console.print(f"\n[bold]🌐 Network Info:[/bold]")
    console.print(f"🔹 Data Sent: {net_io.bytes_sent / (1024 ** 2):.2f} MB")
    console.print(f"🔹 Data Received: {net_io.bytes_recv / (1024 ** 2):.2f} MB")
    
    if net_errors:
        console.print(f"[red]⚠️ Network Errors Detected:[/red] {net_errors}")

    services = ["ssh", "apache2", "nginx", "mysql", "docker"]
    active_services = []
    
    for service in services:
        status = subprocess.run(f"systemctl is-active {service}", shell=True, capture_output=True, text=True).stdout.strip()
        if status == "active":
            active_services.append(service)
    
    console.print(f"\n[bold]🛠️ Running Services:[/bold] {', '.join(active_services) if active_services else '[red]None[/red]'}")

    logs = subprocess.run("journalctl -p 3 -n 20 --no-pager", shell=True, capture_output=True, text=True).stdout.strip()
    
    console.print("\n[bold]🔥 Recent System Errors:[/bold]")
    console.print(logs if logs else "[green]No recent critical errors found.[/green]")

    console.print("\n[bold green]✅ System Diagnostics Completed![/bold green]\n")

def check_for_updates():
    console.print("[yellow]Checking for updates...[/yellow]")
    for step in track(range(10), description="Applying updates..."):
        time.sleep(0.1)
    subprocess.run("git pull origin main", shell=True)
    console.print("[green]Updates applied successfully (if any).[/green]")

if __name__ == "__main__":
    while True:
        choice = display_menu()

        if choice == "1":
            monitor_logs()
        elif choice == "2":
            console.print("[yellow]View Error History: Feature coming soon.[/yellow]")
            show_history()
        elif choice == "3":
            gather_diagnostics()
        elif choice == "4":
            console.print("[yellow]Settings feature coming soon![/yellow]")
        elif choice == "5":
            check_for_updates()
        elif choice == "6":
            console.print("[green]Exiting AI Assistant.[/green]")
            break

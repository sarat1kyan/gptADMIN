                                             
             _   _____ ____  _____ _____ _____ 
     ___ ___| |_|  _  |    \|     |     |   | |
    | . | . |  _|     |  |  | | | |-   -| | | |
    |_  |  _|_| |__|__|____/|_|_|_|_____|_|___|
    |___|_|                                    


# gptADMIN
Sysadmin Assistant with ChatGPT

    A Python tool that assists Linux sysadmins in diagnosing errors, interacting with ChatGPT for troubleshooting, and receiving real-time assistance.

## Overview

The Sysadmin Assistant is a utility designed to enhance the efficiency of Linux system administrators by combining error monitoring, real-time chat with ChatGPT, and system information display. This tool actively monitors system logs for errors, allows users to initiate chat sessions with ChatGPT for detailed troubleshooting, and provides system information relevant to the issues.

## Features

- Real-time error monitoring from system logs.
- Interactive chat sessions with ChatGPT for detailed troubleshooting.
- Display of system information, including distribution, version, kernel, CPU, RAM, and more.

## Installation

1. Clone this repository to your local machine.
2. Run the setup script to install required packages and configure your API key:
    ```bash
    chmod +x gptADMIN.sh
    ./gptADMIN.sh
    ```
3. The setup script will prompt you to enter your OpenAI API key. Make sure to have an OpenAI account and generate an API key.

## Usage

1. Once the setup is complete, run the main script using the following command:
    ```bash
    python3 gptADMIN.py
    ```
2. The script will start monitoring system logs for errors.
3. When an error is detected, you'll have the option to initiate a chat session with ChatGPT for troubleshooting. Follow the on-screen prompts to interact with ChatGPT.
4. To exit the chat session, type 'exit' or 'quit' when prompted by ChatGPT.
5. You can stop the Sysadmin Assistant by pressing Ctrl+C.

## Output example

Sysadmin Assistant is running. Press Ctrl+C to stop.
...
Error: Disk space is running low.
System Info:
  Distributor ID: CentOS
  Description: CentOS Linux 8
  Release: 8.4.2105
  Kernel: 4.18.0-305.12.1.el8_4.x86_64
  CPU: AMD Ryzen 7 3700X 8-Core Processor
  RAM: 15.53 GB
Disk Space: 50% used
...
ChatGPT: Do you want to open a chat session to discuss more about this error? (yes/no)
You: yes
ChatGPT: Initiating chat session...
ChatGPT: Hello! How can I assist you today?
You: I'm getting a low disk space error on my CentOS system.
ChatGPT: Low disk space issues can occur due to a variety of reasons. To address this:
1. Identify large files or directories using the 'du' command.
2. Consider removing unnecessary files or moving them to external storage.
3. Check if there are log files consuming space and manage them appropriately.
...
You: Thanks for the suggestions. Could you provide more details about using the 'du' command?
ChatGPT: Certainly! The 'du' command stands for "disk usage" and helps you identify disk space usage of files and directories. For example, 'du -h' displays human-readable sizes, and 'du -h --max-depth=1' shows usage of top-level directories.
You: That's helpful. How can I check if log files are taking up a lot of space?
ChatGPT: To find large log files, you can use 'find /var/log -type f -size +100M' to locate files larger than 100MB in the '/var/log' directory.
...
You: Thanks for the assistance. I'll follow these steps to manage disk space.
ChatGPT: You're welcome! If you have any more questions, feel free to ask. Good luck!
You: Thank you, goodbye!
ChatGPT: Goodbye!
...
You: exit
ChatGPT: Ending chat session. Have a great day!

## Warning

- Be cautious when running scripts with elevated privileges, as they can potentially modify system configurations or files.
- Ensure that you understand the implications of the actions you take based on the information provided by ChatGPT.
- Always review and validate the responses from ChatGPT before implementing any changes on your system.

---

Feel free to contribute to my project by creating pull requests or reporting issues

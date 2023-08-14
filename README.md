                                             
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

## Warning

- Be cautious when running scripts with elevated privileges, as they can potentially modify system configurations or files.
- Ensure that you understand the implications of the actions you take based on the information provided by ChatGPT.
- Always review and validate the responses from ChatGPT before implementing any changes on your system.

---

Feel free to contribute to this project by creating pull requests or reporting issues.

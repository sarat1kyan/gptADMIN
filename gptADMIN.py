import os
import re
import time
import platform
import openai

# Replace 'YOUR_OPENAI_API_KEY' with your actual OpenAI API key, or write down while running gptADMIN.sh
openai.api_key = 'YOUR_OPENAI_API_KEY'

def chat_with_gpt():
    print("ChatGPT: Hello! How can I assist you today?")
    conversation = []
    
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit']:
            print("ChatGPT: Goodbye!")
            break
        
        conversation.append(f"You: {user_input}")
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversation
        )
        
        message = response.choices[0].message['content']
        conversation.append({"role": "assistant", "content": message})
        print(f"ChatGPT: {message}")

def main():
    print("Sysadmin Assistant is running. Press Ctrl+C to stop.")
    try:
        while True:
            # Read the terminal error messages
            with os.popen('dmesg -T') as dmesg_output:
                error_messages = dmesg_output.read()

            # Extract error messages using regex
            error_pattern = re.compile(r'\[.*\] (.*error.*)', re.IGNORECASE)
            matches = error_pattern.findall(error_messages)

            # Process error messages and initiate chat with ChatGPT
            for error in matches:
                print("\033[1;31mError:\033[0m", error)
                print("\033[1mSystem Info:\033[0m\n", system_info)
                
                print("ChatGPT: Do you want to open a chat session to discuss more about this error? (yes/no)")
                user_choice = input("You: ")
                if user_choice.lower() == 'yes':
                    print("ChatGPT: Initiating chat session...")
                    chat_with_gpt()

                print("=" * 50)

            # Sleep for a while before checking for new errors
            time.sleep(60)  # Adjust the sleep interval as needed

    except KeyboardInterrupt:
        print("\033[1mStopping Sysadmin Assistant.\033[0m")

if __name__ == "__main__":
    main()

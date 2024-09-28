import asyncio
import aiohttp
import sys
import datetime
import random
import string
import os
from termcolor import colored
from replit import clear

now = datetime.datetime.now()
now = now.strftime("%H:%M:%S")
#print now with grey color



if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

menu_color = colored('[/] Menu >> ', 'light_magenta')
spam_color = colored('[/] Spammer >> ', 'light_magenta')
debug_color = colored('[/] Debug >> ', 'light_green')
success_color = colored('[SUCCESS] ', 'light_green')
failed_color = colored('[FAILED] ', 'light_red')

debug_color = colored('[/] Debug >> ', 'light_green')

token_file = 'token.txt'
if os.path.exists(token_file):
    with open(token_file, 'r') as f:
        token_path = f.read().strip()  # Read the path to accs.txt
else:
    print(f"{debug_color}Token path not found in token.txt. Please set a new token with the menu.")
    exit()

    # Now, read the actual tokens from the path inside 'token.txt'
if os.path.exists(token_path):
    with open(token_path, 'r') as f:
        tokens = f.read().splitlines()  # Split tokens by lines to handle multiple tokens
else:
    print(f"T{debug_color}oken file {token_path} not found.")
    exit()

    # Function to blur the last 10 characters of each token for the debug output
def blur_token(token):
    if len(token) > 10:
        return token[:-10] + '*' * 10  # Blur the last 10 characters
    return '*' * len(token)  # If token length is less than 10, blur the entire token

# Debugging output to ensure tokens are loaded, but with last 10 characters blurred
blurred_tokens = [blur_token(token.strip()) for token in tokens]  # Strip each token
print(f"{debug_color}Tokens loaded:\n" + "\n".join(blurred_tokens))  # Print each token on a new line

# Alternate between tokens
token_index = 0

print("")  # Gives space for the spammer
channel = input(f"{spam_color}Enter channel ID: ")
messages = input(f"{spam_color}What message to send?: ")



start = input(f"{spam_color}Start? y/n: ")

if start.lower() == 'y':
    print(f"{spam_color}Running script... (Press Ctrl+C to stop)")
    clear()
    print("\n")
    run = True
elif start.lower() == 'n':
    print(f"{spam_color}ok")
    run = False
    exit()
else:
    print(f"{spam_color}Invalid response. Exiting...")
    exit()

total_messages = 1

# Function to generate random 8-character string
def generate_random_string():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

async def send_message(session, url, headers, payload):
    global total_messages
    async with session.post(url, data=payload, headers=headers) as response:
        if response.status == 200:
            print(f"{now} {success_color}Sent {payload['content']} | Total messages sent: {total_messages}")
            total_messages += 1
        else:
            print(f"{failed_color}Failed to send message. Status code: {response.status}")

async def main():
    global run
    url = f'https://discord.com/api/v9/channels/{channel}/messages'
    
    async with aiohttp.ClientSession() as session:
        while run:
            tasks = []  # Create a list to hold tasks for concurrent sending
            for token in tokens:  # Loop through each token
                headers = {'authorization': token.strip()}
                
                for _ in range(1):
                    payload = {
                        'content': messages,
                    }
                    task = asyncio.create_task(send_message(session, url, headers, payload))
                    tasks.append(task)

            await asyncio.gather(*tasks)  # Send all tasks concurrently

            # Introduce a short delay to avoid hitting rate limits
            await asyncio.sleep(0.1)  # Adjust this delay as needed

if run:
    asyncio.run(main())

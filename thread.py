import asyncio
import aiohttp
import sys
import datetime
import random
import string
import os
from termcolor import colored
from replit import clear

menu_color = colored('[/] Menu >> ', 'light_magenta')
thread_color = colored('[/] Threader >> ', 'light_magenta')
debug_color = colored('[/] Debug >> ', 'light_green')
success_color = colored('[SUCCESS] ', 'light_green')
failed_color = colored('[FAILED] ', 'light_red')

debug_color = colored('[/] Debug >> ', 'light_green')

now = datetime.datetime.now()
now = now.strftime("%H:%M:%S")

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

token_index = 0
print("")

thread_name = input(f"{thread_color}Name: ")
channel = input(f"{thread_color}Enter channel ID: ")

start = input(f"{thread_color}Start? y/n: ")

if start.lower() == 'y':
    print(f"{thread_color}Running script... (Press Ctrl+C to stop)")
    clear()
    print("\n")
    run = True
elif start.lower() == 'n':
    print(f"{thread_color}ok")
    run = False
    exit()
else:
    print(f"{thread_color}Invalid response. Exiting...")
    exit()



total_threads = 1

async def send_message(session, url, headers, payload):
    global total_threads
    try:
        async with session.post(url, json=payload, headers=headers) as response:
            if response.status == 201:
                print(f"{now} {success_color}Sent {payload['name']} | Total threads created: {total_threads}")
                total_threads += 1
            elif response.status == 429:
                retry_after = int(response.headers.get('Retry-After', 1))
                print(f"{failed_color}No permission.")
                await asyncio.sleep(retry_after)  # Wait for the specified time before retrying
            else:
                print(f"{failed_color}Failed to create thread. Status code: {response.status} - {await response.text()}")
    except Exception as e:
        print(f"{failed_color}An error occurred: {str(e)}")

async def main():
    global run
    url = f'https://discord.com/api/v10/channels/{channel}/threads'
    
    async with aiohttp.ClientSession() as session:
        while run:
            tasks = []
            for token in tokens:
                headers = {
                    'authorization': token.strip(),
                    'Content-Type': 'application/json'
                }
                
                payload = {
                    'name': thread_name,
                    'auto_archive_duration': 60,
                    'type': 11
                }
                
                task = asyncio.create_task(send_message(session, url, headers, payload))
                tasks.append(task)

            await asyncio.gather(*tasks)

            # Introduce a longer delay after processing all tasks
            await asyncio.sleep(1)  # Adjust this delay as needed


if run:
    asyncio.run(main())
import asyncio
import aiohttp
import sys
import datetime
import os
from termcolor import colored

menu_color = colored('[/] Menu >> ', 'light_magenta')
debug_color = colored('[/] Debug >> ', 'light_green')
success_color = colored('[SUCCESS] ', 'light_green')
failed_color = colored('[FAILED] ', 'light_red')
checker_color = colored('[CHECKER] >> ', 'yellow')

now = datetime.datetime.now()
now = now.strftime("%H:%M:%S")

token_file = 'token.txt'

# Check if the token file exists
if os.path.exists(token_file):
    with open(token_file, 'r') as f:
        token_path = f.read().strip()  # Read the path to tokens file
else:
    print(f"{debug_color}Token path not found in token.txt. Please set a new token with the menu.")
    exit()

# Read the actual tokens from the path inside 'token.txt'
if os.path.exists(token_path):
    with open(token_path, 'r') as f:
        tokens = f.read().splitlines()  # Split tokens by lines to handle multiple tokens
else:
    print(f"{debug_color}Token file {token_path} not found.")
    exit()

# Function to blur the last 10 characters of each token for debug output
def blur_token(token):
    if len(token) > 10:
        return token[:-10] + '*' * 10  # Blur the last 10 characters
    return '*' * len(token)  # If token length is less than 10, blur the entire token

# Debugging output to ensure tokens are loaded, but with last 10 characters blurred
blurred_tokens = [blur_token(token.strip()) for token in tokens]
print(f"{debug_color}Tokens loaded:\n" + "\n".join(blurred_tokens))

# Input for the guild (server) ID
guild_id = input(f"{checker_color}Enter Server ID: ")

async def get_guild_members(session, url, headers):
    try:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                members = await response.json()
                user_ids = [member['user']['id'] for member in members]  # Extract user IDs
                print(f"{success_color}Members:")
                for user_id in user_ids:
                    print(user_id)
                return True  # Indicate success
            elif response.status == 429:
                retry_after = int(response.headers.get('Retry-After', 1))
                print(f"{failed_color}Rate limit hit. Retry after {retry_after} seconds.")
                await asyncio.sleep(retry_after)  # Wait for the specified time before retrying
            else:
                print(f"{failed_color}Failed to get members. Status code: {response.status} - {await response.text()}")
                return False  # Indicate failure
    except Exception as e:
        print(f"{failed_color}An error occurred: {str(e)}")
        return False  # Indicate failure

async def main():
    url = f'https://discord.com/api/v10/guilds/{guild_id}/members?limit=1000'
    
    async with aiohttp.ClientSession() as session:
        for token in tokens:
            headers = {
                'Authorization': token.strip(),  # Use as a bot token
                'Content-Type': 'application/json'
            }
            success = await get_guild_members(session, url, headers)
            if success:
                break  # Exit the loop if successful
            else:
                print(f"{failed_color}Trying next token...")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"{failed_color}An error occurred in the main loop: {str(e)}")



import requests
from urllib.parse import urlparse

def join(token, server_invite):
    """
    Join a Discord server using the provided token and invite code.

    Args:
        token (str): The Discord token to use for joining the server.
        server_invite (str): The invite code for the server to join.

    Returns:
        bool: True if the join was successful, False otherwise.
    """
    header = {'authorization': token}
    try:
        response = requests.post(f"https://discord.com/api/v9/invites/{server_invite}", headers=header)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error joining server: {e}")
        return False

def get_invite_code(invite_link):
    """
    Extract the invite code from a Discord invite link.

    Args:
        invite_link (str): The Discord invite link.

    Returns:
        str: The invite code extracted from the link.
    """
    parsed_url = urlparse(invite_link)
    return parsed_url.path.split("/")[-1]

def main():
    token_path = input("Enter tokens file path: ")
    invite_link = input("Server link: ")

    # Check if the token file exists and can be read
    try:
        with open(token_path, 'r') as file:
            tokens = file.read().splitlines()
    except FileNotFoundError:
        print("Error: Token file not found.")
        return

    invite_code = get_invite_code(invite_link)

    for token in tokens:
        if join(token, invite_code):
            print("Joining completed.")
        else:
            print("Failed to join server.")

if __name__ == "__main__":
    main()
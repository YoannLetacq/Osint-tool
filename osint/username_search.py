import requests
import json
import random
from .user_agents import USER_AGENTS


# Proceed with a username search on different sites and check if username is used
def search_username(username):
    # Load the sites.json file
    with open("sites.json") as f:
        sites = json.load(f)

    results = {}

    # Randomly select a user agent
    headers = {
        "User-Agent": random.choice(USER_AGENTS)
    }

    # Iterate over the sites and check if the username exists
    for network, url in sites.items():
        try:
            query_url = url.format(username=username)
            response = requests.get(query_url, headers=headers)

            if response.status_code == 200:
                print(f"[+] Found {username} on {network}")

            else:
                print(f"[-] {username} not found on {network}")

        except requests.exceptions.RequestException as e:
            results[f"{network}"] = f"Error checking {network}: {str(e)}"

    return results


import requests
import random
from bs4 import BeautifulSoup
from .user_agents import USER_AGENTS


# Proceed a full name search using Google Dorks and 118000.fr
def search_full_name(firstname, lastname, show_details=False):
    # Load the dork.txt file
    with open("dork.txt") as f:
        dorks = f.readlines()

    results = {
        'firstname': firstname,
        'lastname': lastname,
        'address': None,
        'phone': None,
        'details': []
    }
    full_name = f"{firstname} {lastname}"

    # Randomly select a user agent
    headers = {
        "User-Agent": random.choice(USER_AGENTS)
    }

    # Iterate over the dork URLs and perform the search
    for dork in dorks:
        dork = dork.strip()
        query_url = dork.format(full_name)
        try:
            response = requests.get(query_url, headers=headers)
            if response.status_code == 200:
                results['details'].append(f"Results found using: {query_url}")
            else:
                results['details'].append(f"No results using: {query_url}")
        except requests.exceptions.RequestException as e:
            results['details'].append(f"Error using dork: {query_url} - {str(e)}")

    # Perform search on 118000.fr
    try:
        search_url = f"https://www.118000.fr/search?who={firstname}+{lastname}"
        response = requests.get(search_url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            # Extract address and phone number
            address = soup.find('div', class_='h4 address mtreset')
            phone = soup.find('div', class_='phone h2')

            if address:
                results['address'] = address.get_text(separator=' ', strip=True)
            if phone:
                phone_number = phone.find('a', class_='clickable atel')
                if phone_number:
                    results['phone'] = phone_number.get_text(strip=True)

            results['details'].append(f"Results found on 118000.fr for {full_name}")
        else:
            results['details'].append(f"No results on 118000.fr for {full_name}")
    except requests.exceptions.RequestException as e:
        results['details'].append(f"Error using 118000.fr: {str(e)}")

    # Format the output
    formatted_result = (
        f"First Name: {results['firstname']}\n"
        f"Last Name: {results['lastname']}\n"
        f"Address: {results['address'] or 'N/A'}\n"
        f"Phone: {results['phone'] or 'N/A'}\n"
    )

    if show_details:
        formatted_result += "\nDetails:\n" + "\n".join(results['details'])

    return formatted_result

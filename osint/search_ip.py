import requests


# Made an ip search using ipInfo
def search_ip(ip):

    try:
        # request to ipinfo
        response = requests.get(f"https://ipinfo.io/{ip}")
        response.raise_for_status()

        if response.status_code == 200:
            data = response.json()
            location = data.get('loc', 'N/A').split(',')
            latitude = location[0] if len(location) > 1 else 'N/A'
            longitude = location[1] if len(location) > 1 else 'N/A'

            result = (
                f"IP: {ip}\n"
                f"ISP: {data.get('org', 'N/A')}\n"
                f"City: {data.get('city', 'N/A')}\n"
                f"Latitude: {latitude}\n"
                f"Longitude: {longitude}\n"
            )
            return result

    except requests.exceptions.HTTPError as err:
        print(err)
        return {"error": "Failed to retrieve IP information."}

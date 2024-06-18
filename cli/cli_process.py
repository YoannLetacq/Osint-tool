import argparse
from osint.full_name_search import search_full_name
from osint.username_search import search_username
from osint.search_ip import search_ip


def main_cli():
    parser = argparse.ArgumentParser(description="OSINT CLI Tool")
    parser.add_argument('-fn', '--fullname', nargs=2, metavar=('FIRSTNAME', 'LASTNAME'), help='Search for a person by full name')
    parser.add_argument('-u', '--username', metavar='USERNAME', help='Search for a username on different social networks')
    parser.add_argument('-ip', '--ipaddress', metavar='IPADDRESS', help='Search for information about an IP address')
    parser.add_argument('--detail', action='store_true', help='Show detailed search results')

    args = parser.parse_args()

    if args.fullname:
        firstname, lastname = args.fullname
        result = search_full_name(firstname, lastname, show_details=args.detail)
        print(result)
    elif args.username:
        result = search_username(args.username)
        print(result)
    elif args.ipaddress:
        result = search_ip(args.ipaddress)
        print(result)
    else:
        parser.print_help()


if __name__ == "__main__":
    main_cli()

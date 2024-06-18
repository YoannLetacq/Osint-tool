from cli.cli_process import main_cli
from osint.full_name_search import search_full_name
from osint.username_search import search_username
from osint.search_ip import search_ip


def run_tests():
    print("Running tests with hardcoded parameters...\n")

    print("Testing full name search:")
    full_name_result = search_full_name("Jean", "Dupont")
    print(full_name_result)
    print("\n")

    print("Testing username search:")
    username_result = search_username("testuser")
    print(username_result)
    print("\n")

    print("Testing IP search:")
    ip_result = search_ip("8.8.8.8")
    print(ip_result)
    print("\n")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    else:
        main_cli()

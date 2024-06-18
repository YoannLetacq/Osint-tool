import unittest
import requests
from unittest.mock import patch, mock_open
from osint.full_name_search import search_full_name


class TestSearchFullName(unittest.TestCase):

    @patch('osint.full_name_search.requests.get')
    @patch('builtins.open', new_callable=mock_open, read_data=(
            'https://www.google.com/search?q=intext:(%22{}%22)\n'
            'https://www.google.com/search?q=intext:(%22{}%22)+filetype:pdf\n'
    ))
    def test_search_full_name_success(self, mock_open, mock_get):
        # Mock the successful response from Google Dork search and 118000.fr
        mock_response = unittest.mock.Mock()
        mock_response.status_code = 200
        mock_response.content = '''
            <html>
            <div class="h4 address mtreset">1465 AVENUE DE MAURIN<br>34000 Montpellier</div>
            <div class="phone h2 "><a href="tel:0467278287" class="clickable atel" aria-label="Ouvrir numéro">04 67 27 82 87</a></div>
            </html>
        '''
        mock_get.return_value = mock_response

        firstname = 'Jean'
        lastname = 'Dupont'
        result = search_full_name(firstname, lastname)
        expected = {
            'firstname': firstname,
            'lastname': lastname,
            'address': '1465 AVENUE DE MAURIN 34000 Montpellier',
            'phone': '04 67 27 82 87',
            'details': [
                f"Results found using: https://www.google.com/search?q=intext:(%22{firstname} {lastname}%22)",
                f"Results found using: https://www.google.com/search?q=intext:(%22{firstname} {lastname}%22)+filetype:pdf",
                f"Results found on 118000.fr for {firstname} {lastname}"
            ]
        }
        self.assertEqual(result, expected)

    @patch('osint.full_name_search.requests.get')
    @patch('builtins.open', new_callable=mock_open, read_data=(
            'https://www.google.com/search?q=intext:(%22{}%22)\n'
            'https://www.google.com/search?q=intext:(%22{}%22)+filetype:pdf\n'
    ))
    def test_search_full_name_no_results(self, mock_open, mock_get):
        # Mock the no results response from Google Dork search and 118000.fr
        mock_response = unittest.mock.Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        firstname = 'Jedddddddddddddddddddddddddddddddddddddddddddddddddddddddddddan'
        lastname = 'Duzdzpont'
        result = search_full_name(firstname, lastname)
        expected = {
            'firstname': firstname,
            'lastname': lastname,
            'address': None,
            'phone': None,
            'details': [
                f"No results using: https://www.google.com/search?q=intext:(%22{firstname} {lastname}%22)",
                f"No results using: https://www.google.com/search?q=intext:(%22{firstname} {lastname}%22)+filetype:pdf",
                f"No results on 118000.fr for {firstname} {lastname}"
            ]
        }
        self.assertEqual(result, expected)

    @patch('osint.full_name_search.requests.get')
    @patch('builtins.open', new_callable=mock_open, read_data=(
            'https://www.google.com/search?q=intext:(%22{}%22)\n'
            'https://www.google.com/search?q=intext:(%22{}%22)+filetype:pdf\n'
    ))
    def test_search_full_name_error(self, mock_open, mock_get):
        # Mock the error response from Google Dork search and 118000.fr
        mock_get.side_effect = requests.exceptions.RequestException("Network error")

        firstname = 'John'
        lastname = 'Doe'
        result = search_full_name(firstname, lastname)
        expected = {
            'firstname': firstname,
            'lastname': lastname,
            'address': None,
            'phone': None,
            'details': [
                f"Error using dork: https://www.google.com/search?q=intext:(%22{firstname} {lastname}%22) - Network error",
                f"Error using dork: https://www.google.com/search?q=intext:(%22{firstname} {lastname}%22)+filetype:pdf - Network error",
                f"Error using 118000.fr: Network error"
            ]
        }
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()

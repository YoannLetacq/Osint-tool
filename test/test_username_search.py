import requests
import json
import unittest
from unittest.mock import patch, mock_open
from osint.username_search import search_username


class TestSearchUsername(unittest.TestCase):

    @patch('osint.username_search.requests.get')
    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps({
        "facebook": "https://www.facebook.com/{username}",
        "twitter": "https://twitter.com/{username}",
        "linkedin": "https://www.linkedin.com/in/{username}",
        "instagram": "https://www.instagram.com/{username}"
    }))
    def test_search_username_success(self, mock_open, mock_get):
        # Mock the successful responses from social networks
        mock_response = unittest.mock.Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        username = 'yoannletacq'
        result = search_username(username)
        expected = {
            "instagram": f"Username '{username}' found on instagram: https://www.instagram.com/{username}"
        }
        self.assertEqual(result, expected)

    @patch('osint.username_search.requests.get')
    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps({
        "facebook": "https://www.facebook.com/{username}",
        "twitter": "https://twitter.com/{username}",
        "linkedin": "https://www.linkedin.com/in/{username}",
        "instagram": "https://www.instagram.com/{username}"
    }))
    def test_search_username_not_found(self, mock_open, mock_get):
        # Mock the not found responses from social networks
        mock_response = unittest.mock.Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        username = 'testfefefefefuser'
        result = search_username(username)
        expected = {
            "facebook": f"Username '{username}' not found on facebook",
            "twitter": f"Username '{username}' not found on twitter",
            "linkedin": f"Username '{username}' not found on linkedin",
            "instagram": f"Username '{username}' not found on instagram"
        }
        self.assertEqual(result, expected)

    @patch('osint.username_search.requests.get')
    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps({
        "facebook": "https://www.facebook.com/{username}",
        "twitter": "https://twitter.com/{username}",
        "linkedin": "https://www.linkedin.com/in/{username}",
        "instagram": "https://www.instagram.com/{username}"
    }))
    def test_search_username_error(self, mock_open, mock_get):
        # Mock the error responses from social networks
        mock_get.side_effect = requests.exceptions.RequestException("Network error")

        username = 'testu<rfg<srg<rg<qser'
        result = search_username(username)
        expected = {
            "facebook": "Error checking facebook: Network error",
            "twitter": "Error checking twitter: Network error",
            "linkedin": "Error checking linkedin: Network error",
            "instagram": "Error checking instagram: Network error"
        }
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()

import unittest
from unittest.mock import patch

import requests
from osint.search_ip import search_ip


class TestSearchIP(unittest.TestCase):

    @patch('osint.search_ip.requests.get')
    def test_search_ip_success(self, mock_get):
        # Mock the response from ipinfo.io
        mock_response = unittest.mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'org': 'Mock ISP',
            'city': 'Mock City',
            'loc': '12.34,56.78'
        }
        mock_get.return_value = mock_response

        ip = '8.8.8.8'
        result = search_ip(ip)
        expected = {
            'ip': ip,
            'isp': 'Mock ISP',
            'city': 'Mock City',
            'latitude': '12.34',
            'longitude': '56.78'
        }
        self.assertEqual(result, expected)

    @patch('osint.search_ip.requests.get')
    def test_search_ip_failure(self, mock_get):
        # Mock the response from ipinfo.io for an invalid IP address
        mock_response = unittest.mock.Mock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError
        mock_get.return_value = mock_response

        ip = '999.999.999.999'
        result = search_ip(ip)
        expected = {"error": "Failed to retrieve IP information."}
        self.assertEqual(result, expected)

    @patch('osint.search_ip.requests.get')
    def test_search_ip_no_location(self, mock_get):
        # Mock the response from ipinfo.io
        mock_response = unittest.mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'org': 'Mock ISP',
            'city': 'Mock City',
            'loc': 'N/A'
        }
        mock_get.return_value = mock_response

        ip = '8.8.8.8'
        result = search_ip(ip)
        expected = {
            'ip': ip,
            'isp': 'Mock ISP',
            'city': 'Mock City',
            'latitude': 'N/A',
            'longitude': 'N/A'
        }
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()

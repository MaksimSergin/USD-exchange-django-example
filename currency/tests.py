from django.test import TestCase, Client
from django.core.cache import cache
from unittest.mock import patch
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta

class ExchangeRateTestCase(TestCase):
    def setUp(self):
        cache.clear()
        cache.set("RECENT_REQUESTS", [], timeout=None)
        self.client = Client()
        self.url = reverse('get_current_usd')

    def tearDown(self):
        cache.clear()

    @patch("currency.views.requests.get")
    def test_get_current_usd_rate(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"rates": {"RUB": 100.0}}

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("rate", data)
        self.assertEqual(data["rate"], 100.0)
        self.assertIn("recent_requests", data)
        self.assertEqual(len(data["recent_requests"]), 1)
        self.assertEqual(data["message"], "Data retrieved from external API")

    @patch("currency.views.requests.get")
    def test_request_limit_and_recent_requests_list(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"rates": {"RUB": 100.0}}

        with patch("currency.views.timezone") as mock_timezone:
            base_time = timezone.now()
            for i in range(11):
                mock_timezone.now.return_value = base_time + timedelta(seconds=i * 600)
                response = self.client.get(self.url)

        data = response.json()
        self.assertEqual(len(data["recent_requests"]), 10)
        self.assertEqual(data["recent_requests"][0][1], 100.0)

        response = self.client.get(self.url)
        self.assertEqual(response.json()["message"], "Data returned from cache")

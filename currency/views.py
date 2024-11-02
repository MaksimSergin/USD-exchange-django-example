import requests
from django.core.cache import cache
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta

API_URL = 'https://api.exchangerate-api.com/v4/latest/USD'
CACHE_TIMEOUT = 10
TIMEZONE_OFFSET = timedelta(hours=3)
RECENT_REQUESTS_LIMIT = 10

def get_current_usd(request):
    current_time = timezone.now()
    cached_rate = cache.get('USD_EXCHANGE_RATE')
    last_request_time = cache.get('LAST_REQUEST_TIME')
    recent_requests = cache.get('RECENT_REQUESTS', [])

    if cached_rate and last_request_time:
        time_since_last_request = (current_time - last_request_time).total_seconds()
        if time_since_last_request < CACHE_TIMEOUT:
            adjusted_timestamp = (last_request_time + TIMEZONE_OFFSET).isoformat()
            return JsonResponse({
                'timestamp': adjusted_timestamp,
                'rate': float(cached_rate),
                'recent_requests': recent_requests,
                'message': 'Data returned from cache'
            })

    try:
        response = requests.get(API_URL, timeout=5)
        response.raise_for_status()
        data = response.json()
        usd_to_rub_rate = data.get('rates', {}).get('RUB')

        if usd_to_rub_rate is None:
            raise ValueError("RUB rate not found in API response.")

        cache.set('USD_EXCHANGE_RATE', usd_to_rub_rate, timeout=CACHE_TIMEOUT)
        cache.set('LAST_REQUEST_TIME', current_time, timeout=CACHE_TIMEOUT)

        adjusted_current_time = (current_time + TIMEZONE_OFFSET).isoformat()
        recent_requests = [(adjusted_current_time, float(usd_to_rub_rate))] + recent_requests[:RECENT_REQUESTS_LIMIT - 1]
        cache.set('RECENT_REQUESTS', recent_requests, timeout=None)

        return JsonResponse({
            'timestamp': adjusted_current_time,
            'rate': float(usd_to_rub_rate),
            'recent_requests': recent_requests,
            'message': 'Data retrieved from external API'
        })

    except requests.RequestException:
        return JsonResponse({'error': 'Error fetching data from external API.'}, status=500)
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=500)

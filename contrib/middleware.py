import time
from django.http import JsonResponse
from django.conf import settings
from django.core.cache import cache
from django.shortcuts import render


class ThrottlingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Request limit configurations
        self.requests_limit = getattr(settings, 'THROTTLE_REQUESTS_LIMIT', 100)  # Limit of 100 requests per IP
        self.time_window = getattr(settings, 'THROTTLE_TIME_WINDOW', 60)  # Time window of 60 seconds
        self.cache_timeout = getattr(settings, 'THROTTLE_CACHE_TIMEOUT', self.time_window)  # Cache expiration time

    def __call__(self, request):
        # Check if the request is for /api/ or other routes
        user_ip = self.get_client_ip(request)
        cache_key = f"throttle_{user_ip}"

        # Retrieve the requests stored in the cache
        requests = cache.get(cache_key, [])

        current_time = time.time()

        # Filter out old requests
        requests = [timestamp for timestamp in requests if current_time - timestamp < self.time_window]

        # Check if the request limit has been reached
        if len(requests) >= self.requests_limit:
            # If it's an API request, return a JSON error
            if request.path.startswith('/api/'):
                return JsonResponse({
                    'error': 'Too many requests. Please try again later.',
                    'status': 429
                }, status=429)
            # If it's a normal page, return an HTML error page
            else:
                return self.throttle_error_page(request)

        # Log the new request in the cache
        requests.append(current_time)
        cache.set(cache_key, requests, timeout=self.cache_timeout)

        # Call the original view
        response = self.get_response(request)

        # Force the response to be JSON for API or HTML for normal pages
        if request.path.startswith('/api/'):
            response['Content-Type'] = 'application/json'  # Ensure that responses for /api/ are in JSON
        else:
            response['Content-Type'] = 'text/html'  # Ensure that other responses are in HTML

        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def throttle_error_page(self, request):
        return render(request, 'error/throttle.html', {
            'message': 'Too many requests. Please try again later.'
        })
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

    def __call__(self, request):
        # Check if the request is for /api/ or other routes
        user_ip = self.get_client_ip(request)
        cache_key = f"throttle_{user_ip}"

        # Use atomic operations to increment request count
        try:
            # Attempt to atomically increment the request count
            new_count = cache.incr(cache_key)
        except ValueError:
            # Key doesn't exist, initialize it with 1 and set expiration
            added = cache.add(cache_key, 1, timeout=self.time_window)
            if not added:
                # Race condition: key was added by another request, increment
                try:
                    new_count = cache.incr(cache_key)
                except ValueError:
                    # Fallback in case of rare race condition
                    new_count = 1
            else:
                new_count = 1

        # Check if the request limit has been exceeded
        if new_count > self.requests_limit:
            # Throttle the request
            if request.path.startswith('/api/'):
                return JsonResponse({
                    'error': 'Too many requests. Please try again later.',
                    'status': 429
                }, status=429)
            else:
                return self.throttle_error_page(request)

        # Proceed with the request
        response = self.get_response(request)

        # Set appropriate Content-Type headers
        if request.path.startswith('/api/'):
            response['Content-Type'] = 'application/json'  # Ensure JSON response for APIs
        else:
            response['Content-Type'] = 'text/html'  # Ensure HTML for other pages

        return response

    def get_client_ip(self, request):
        # Get client IP considering X-Forwarded-For header for proxies
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def throttle_error_page(self, request):
        # Render HTML error page for non-API requests
        return render(request, 'error/throttle.html')
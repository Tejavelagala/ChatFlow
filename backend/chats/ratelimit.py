from django.http import JsonResponse
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import decorator_from_middleware_with_args
from django.utils.deprecation import MiddlewareMixin


class RateLimitMiddleware(MiddlewareMixin):
    """Rate limiting for authentication endpoints"""
    
    def process_request(self, request):
        # Rate limit login attempts: 5 per minute per IP
        if request.path == '/auth/jwt/create/' and request.method == 'POST':
            from django_ratelimit.core import get_usage
            from django_ratelimit.exceptions import Ratelimited
            
            try:
                from django_ratelimit.decorators import ratelimit as rl
                key = self.get_client_ip(request)
                
                # Check rate limit
                from django_ratelimit.core import is_rate_limited
                if is_rate_limited(request, 'login', '5/m', key='ip'):
                    return JsonResponse(
                        {'error': 'Too many login attempts. Try again later.'},
                        status=429
                    )
            except Exception:
                pass
        
        # Rate limit registration: 3 per minute per IP
        if request.path == '/auth/users/' and request.method == 'POST':
            try:
                from django_ratelimit.core import is_rate_limited
                if is_rate_limited(request, 'register', '3/m', key='ip'):
                    return JsonResponse(
                        {'error': 'Too many registration attempts. Try again later.'},
                        status=429
                    )
            except Exception:
                pass
        
        return None
    
    @staticmethod
    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

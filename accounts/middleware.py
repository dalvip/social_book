from django.utils.deprecation import MiddlewareMixin

class TokenAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if 'access_token' in request.session:
            request.META['HTTP_AUTHORIZATION'] = f'Bearer {request.session["access_token"]}'
        return None
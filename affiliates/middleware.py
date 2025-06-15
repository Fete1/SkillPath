# affiliates/middleware.py
class AffiliateMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if 'ref' is in the query parameters
        ref_code = request.GET.get('ref')
        if ref_code:
            # If it is, store it in the session
            request.session['affiliate_ref'] = ref_code
        response = self.get_response(request)
        return response
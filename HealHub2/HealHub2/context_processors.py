from django.conf import settings

def google_api_key(request):
    return {'google_api_key': settings.GOOGLE_API_KEY}

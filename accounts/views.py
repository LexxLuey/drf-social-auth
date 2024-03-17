from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.providers.apple.client import AppleOAuth2Client
from allauth.socialaccount.providers.apple.views import AppleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView as DJSocialLoginView
from rest_framework.throttling import UserRateThrottle


class MyThrottle(UserRateThrottle):
    rate = "10/day"


class AppleLogin(SocialLoginView):
    adapter_class = AppleOAuth2Adapter
    callback_url = "http://127.0.0.1:3000/"
    client_class = AppleOAuth2Client
    throttle_classes = [MyThrottle]


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = "http://127.0.0.1:3000/"
    client_class = OAuth2Client
    throttle_classes = [MyThrottle]

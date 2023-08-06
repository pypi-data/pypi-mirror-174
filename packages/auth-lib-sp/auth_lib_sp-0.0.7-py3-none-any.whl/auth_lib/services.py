from rest_framework import authentication
from rest_framework.request import Request
from requests import Response
from .models import TokenUser
import os, requests, jwt

VERIFY_URL = os.environ['VERIFY_URL']

HEADERS = {
    'Content-Type': 'application/json', 
}

def _verify(token: str) -> Response:
    return requests.post(VERIFY_URL, headers=HEADERS, json={"token": token})

class MyJWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request: Request):
        if  'HTTP_AUTHORIZATION' in request.META and token != None:
            token = request.META.get('HTTP_AUTHORIZATION')
            token = token[7:]

            response = _verify(token)
            if response.status_code == 200:
                decode_token = jwt.decode(token, os.environ['SECRET_KEY'], algorithms=['HS256'])
                user = TokenUser()
                user.from_json(decode_token['user'])
                return user, None
            
        return None, None

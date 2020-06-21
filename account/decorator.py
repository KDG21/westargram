import jwt
import json
from django.http import JsonResponse, HttpResponse
from account.models import Account
from westargram.settings import SECRET_KEY

def login_check(func):
    def wrapper(self, request, *args, **kwargs):
        access_token = request.headers.get("Authorization", None)  # request header에 Authorization이나 none을 찾는다.
        if access_token is not None:  # none이 아니면
            try:
                decode_token = jwt.decode(access_token, SECRET_KEY, algorithms='HS256')  # account.id로 토큰 만든것을 다시 디코드하면 account.id 값이 {id : 1}형태로 나온다.
                account_id = decode_token['id'] # id가 1번이면 1로 나옴
                account = Account.objects.get(id=account_id)  # account에 id가 1번이면 1번인 객체를 찾는거
                request.user = account  

                return func(self, request, *args, **kwargs)
            except jwt.DecodeError:  # 없는 토큰값이 들어온경우
                return JsonResponse({'message' : '토큰값이 없습니다.'}, status=400)
            except Account.DoesNotExist:  # 유효한 토큰값이지만 아이디가 없는경우
                return JsonResponse({'message' : '아이디가 존재하지 않습니다.'}, status=400)
        else:  
            return JsonResponse({'message' : '로그인이 필요합니다.'}, status=401)
    return wrapper
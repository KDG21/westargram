from django.shortcuts import render
from account.models import Account
from django.views import View
from django.http import JsonResponse, HttpResponse
from westargram.settings import SECRET_KEY
import json
import bcrypt
import jwt

class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)
        hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt() )
        try:
            if Account.objects.filter(email = data['email']).exists():
                return JsonResponse({'message':'아이디가 존재합니다.'},status=401)
            else:
                Account(
                    email = data['email'],
                    password = hashed_password
                    # password = hashed_password.decode('utf-8')
                ).save()
                return JsonResponse({'message':'회원가입 완료!'},status=200)
        except KeyError:
            return JsonResponse({'message':'key error'},status=400)

    def get(self, request):
        account_data = Account.objects.values()
        return JsonResponse({'data':list(account_data)}, status=200)

class SignInView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            if Account.objects.filter(email = data['email']).exists():
                account = Account.objects.get(email = data['email'])
                # if account.password == data['password']:
                if bcrypt.checkpw(data['password'].encode('utf-8'), account.password):
                    
                    token=jwt.encode({'id':account.id}, SECRET_KEY, algorithm='HS256')
                    return JsonResponse({'access_token':token.decode('utf-8')}, status=200)
                else:
                    return JsonResponse({'message':'패스워드가 틀립니다.'}, status=401)
            else:
                return JsonResponse({'message':'아이디가 존재하지 않습니다.'}, status=401)
            
        except KeyError:
            return JsonResponse({'message':'key error'},status=400)
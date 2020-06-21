from django.shortcuts import render
from account.models import Account
from comment.models import Comment
from django.views import View
from django.http import JsonResponse, HttpResponse
import json
from account.decorator import login_check

class CommentView(View):
    @login_check
    def post(self, request):
        data = json.loads(request.body)
        Comment(
            email = request.user,
            comment = data['comment']
        ).save()

        return JsonResponse({'message' : 'SUCCESS'}, status=200)


    # def get(self, request):
    #     comment_data = Comment.objects.values()
    #     return JsonResponse({'data':list(comment_data)}, status=200)


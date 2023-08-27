from django.shortcuts import render
from django.http import JsonResponse
# Create your views here.
def chatbot(req):
    if req.method == 'POST':
        message = req.POST.get('message')
        response = 'Hello'
        return JsonResponse({'message': message, 'response': response})
    return render(req, 'chatbot.html')
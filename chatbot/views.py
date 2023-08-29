from dotenv import load_dotenv
import os

from django.shortcuts import render, redirect
from django.http import JsonResponse
import openai

from django.contrib import auth
from django.contrib.auth.models import User
from .models import Chat
from django.utils import timezone

load_dotenv()

openai.api_key = os.environ.get("API_KEY")

def askOpenai(message):
    response = openai.ChatCompletion.create(
        model = "gpt-4",
        messages=[
        {"role": "system", "content": "You are a helpful, friendly assistant that answers all questions based on your knowledge."},
        {"role": "user", "content": message}
    ]
    )
    print(response)
    answer = response['choices'][0]['message']['content']
    return answer

def chatbot(req):
    chats = Chat.objects.filter(user=req.user)

    if req.method == 'POST':
        message = req.POST.get('message')
        response = askOpenai(message)
        chat = Chat(user=req.user, message=message, response=response, created_at=timezone.now)
        chat.save()
        return JsonResponse({'message': message, 'response': response})
    return render(req, 'chatbot.html', {'chats': chats})

def login(req):
    if req.method == 'POST':
        username = req.POST['username']
        password = req.POST['password']
        user = auth.authenticate(req, username=username, password=password)
        if user:
            auth.login(req, user)
            return redirect('chatbot')
        else:
            errormsg = "Invalid username or password"
            return render(req, 'login.html', {'error_message': errormsg})
    else:
        return render(req, 'login.html')

def register(req):
    if req.method == 'POST':
        username = req.POST['username']
        email = req.POST['email']
        password1 = req.POST['password1']
        password2 = req.POST['password2']
        if password1 == password2:
            try:
                user = User.objects.create_user(username, email, password1)
                user.save()
                auth.login(req, user)
                return redirect('chatbot')
            except:
                errormsg = "Error creating the account"
                return render(req, 'register.html', {'error_message': errormsg}) 

        else:
            errormsg = "Passwords do not match"
            return render(req, 'register.html', {'error_message': errormsg}) 
    return render(req, 'register.html')

def logout(req):
    auth.logout(req)
    return redirect('login')
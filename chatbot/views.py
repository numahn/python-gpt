from django.shortcuts import render

# Create your views here.
def chatbot(req):
    return render(req, 'chatbot.html')
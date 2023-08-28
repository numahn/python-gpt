from dotenv import load_dotenv
import os
from django.shortcuts import render
from django.http import JsonResponse
import openai

load_dotenv()

openai.api_key = os.environ.get("API_KEY")

def askOpenai(message):
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages=[
        {"role": "system", "content": "You are a helpful, friendly assistant that answers all questions based on your knowledge."},
        {"role": "user", "content": message}
    ]
    )
    print(response)
    answer = response['choices'][0]['message']['content']
    return answer

def chatbot(req):
    if req.method == 'POST':
        message = req.POST.get('message')
        response = askOpenai(message)
        return JsonResponse({'message': message, 'response': response})
    return render(req, 'chatbot.html')
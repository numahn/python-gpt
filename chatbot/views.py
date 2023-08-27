from django.shortcuts import render
from django.http import JsonResponse
import openai

openaiKey = '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'
openai.api_key = openaiKey

def askOpenai(message):
    response = openai.Completion.create(
        model = "text-davinci-003",
        prompt = message,
        max_tokens = 50,
        n = 1,
        stop = None,
        temperature = 0.7,
    )
    answer = response.choices[0].text.strip()
    return answer

def chatbot(req):
    if req.method == 'POST':
        message = req.POST.get('message')
        response = askOpenai(message)
        return JsonResponse({'message': message, 'response': response})
    return render(req, 'chatbot.html')
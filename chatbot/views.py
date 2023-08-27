from django.shortcuts import render
from django.http import JsonResponse
import openai

openaiKey = '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'
openai.api_key = openaiKey

def askOpenai(message):
    # response = openai.Completion.create(
    #     model = "text-davinci-003",
    #     prompt = message,
    #     max_tokens = 150,
    #     n = 1,
    #     stop = None,
    #     temperature = 0.7,
    # )
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages=[
        {"role": "system", "content": "You are a helpful assistant that answers all questions based on your knowledge."},
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
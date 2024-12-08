from django.shortcuts import render
from django.http import JsonResponse
import google.generativeai as genai
from django.views.decorators.csrf import csrf_exempt
import json

# Configure the API
genai.configure(api_key='AIzaSyDNhqim_xonevMWC5ZH0tdZBM6_9d4mue0')

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction=[
        "You are an astrologer appointment booking assistant. Please follow the instructions below:",
        "1. Ask the user for their name, date of birth, and place of birth in Tamil.",
        "2. Provide available time slots from Monday to Friday, from 10:00 AM to 1:00 PM, split into 30-minute intervals.",
        "3. Show only the next 5 upcoming dates for the user to choose from.",
        "4. After the user selects a date, provide the available time slots for that specific date.",
        "5. Ensure the system allows the user to only choose from the available options.",
        "6. All communication should be in Tamil only."
    ]
)

@csrf_exempt
def chatbot_view(request):
    user_input_history = json.loads(request.body.decode('utf-8'))

    if user_input_history:
        chat_session = model.start_chat(history=user_input_history['data']['history'])
        response = chat_session.send_message(user_input_history['data']['user_input'])
        return JsonResponse({"response": response.text})
    else:
        return JsonResponse({"error": "No user input provided."})




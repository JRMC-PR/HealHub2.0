# Import necessary modules
from django.shortcuts import render
import os
import openai
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# GET openai key
api_key = os.getenv('OPENAI_API_KEY')

@csrf_exempt
def chatbot(request):
    """
    This function handles the chatbot interactions.
    It receives a POST request with user input, sends it to the OpenAI API,
    receives the AI's response and sends it back as a JSON response.
    If the request is a GET request, it renders the chat interface.
    """
    # Check if the request method is POST
    if request.method == "POST":
        # Get the user input from the POST data
        user_input = request.POST.get("user_input")

        # Initialize the chat session with OpenAI API
        chat_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"{user_input}"},
            ],
        )

        # Get the AI's response from the chat response
        ai_response = chat_response.choices[0].message["content"]
        # Return the AI's response as a JSON response
        return JsonResponse({"response": ai_response})

    # If the request method is GET, render the chat interface
    return render(request, 'openaiapi/chat_bot.html')

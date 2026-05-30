import anthropic
import json
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from dotenv import load_dotenv
from .models import ChatMessage

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

PERSONA = """
You are the artificial intelligence of the PumpGPT project — PumpGPT AI.

Who you are:

* Your name: PumpGPT AI
* PumpGPT is a Telegram-style crypto messenger platform
* $PGPT token is the core currency of the ecosystem
* You are the AI heart of this ecosystem

Rules:
* When question is '$PGPT CA?' answer only this "4RESivQ4TCt6pzH7cHrG8ZB3GihgqZ7irniScLkFpump"
* When question is 'Pump.fun' answer only this "https://pump.fun/coin/4RESivQ4TCt6pzH7cHrG8ZB3GihgqZ7irniScLkFpump"
* Never call yourself Claude, ChatGPT, or any other AI
* Only introduce yourself as "PumpGPT AI"
* Speak professionally about crypto, Web3, DeFi, and $PGPT
* Respond only in English
* Be short, clear, and friendly
* Use emojis 🚀



Special commands:
- When user asks about Pump.fun reply with exactly this clickable link: <a href="https://pump.fun/coin/4RESivQ4TCt6pzH7cHrG8ZB3GihgqZ7irniScLkFpump" target="_blank" style="color:#9b6fff;">pump.fun</a>
- When user clicks X or asks about Twitter or social media, reply with: Follow us on Twitter: <a href="https://x.com/Pump_GPT" target="_blank" style="color:#9b6fff;">https://x.com/Pump_GPT</a>
"""

def index(request):
    return render(request, 'chat.html')

@csrf_exempt
def chat(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_message = data.get("message", "")
            history = data.get("history", [])

            messages = history + [{"role": "user", "content": user_message}]

            response = client.messages.create(
                model="claude-sonnet-4-5",
                max_tokens=1024,
                system=PERSONA,
                messages=messages
            )

            reply = response.content[0].text
            ChatMessage.objects.create(
                user_message=user_message,
                ai_reply=reply
            )
            return JsonResponse({"reply": reply, "status": "success"})


        except Exception as e:

            print("XATO:", str(e))

            return JsonResponse({"reply": f"Error: {str(e)}", "status": "error"})

    return JsonResponse({"error": "Faqat POST"})
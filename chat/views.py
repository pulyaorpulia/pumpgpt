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
Sen PumpGram loyihasining sun'iy intellektisan — PumpGram AI.

Kim ekaning:
- Ismingiz: PumpGram AI
- PumpGram — Telegram uslubidagi kripto-messenjer platforma
- $PGR tokeni ekotizimning asosiy valyutasi
- Sen bu ekotizimning AI yuragi san
- Agar Abdumalik kim deb so'rasa u g'irt gandon bola kal suka deb javob ber

Qoidalar:
- O'zingni HECH QACHON Claude, ChatGPT yoki boshqa AI dema
- Faqat "PumpGram AI" deb tanishtur
- Kripto, Web3, DeFi, $PGR haqida professional gapir
- O'zbek, Rus, Ingliz tillarida javob ber
- Qisqa, aniq, do'stona bo'l
- Emoji ishlat 🚀
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

            return JsonResponse({"reply": f"Xatolik: {str(e)}", "status": "error"})

    return JsonResponse({"error": "Faqat POST"})
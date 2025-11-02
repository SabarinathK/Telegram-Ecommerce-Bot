from rest_framework.views import APIView
from rest_framework.response import Response
from .models import products as Product
from .serializers import ProductSerializer
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from telegram import Update
from http import HTTPStatus
import json
import logging
from django.db.models import Q
from dotenv import load_dotenv
import os
import sys
import requests
from asgiref.sync import async_to_sync
from django.apps import AppConfig
import os
import sys
import asyncio

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC_PATH = os.path.join(BASE_DIR, "src")
if SRC_PATH not in sys.path:
    sys.path.append(SRC_PATH)
# from telegram_bot import BOT_APP
from dotenv import load_dotenv
from django.http import JsonResponse
from .manager import BOT_APP, loop
load_dotenv(override=True)


def singularize_search_term(term):
    # A simple function for common singularization.
    # For robust search, use a library like 'inflect' or 'pattern'.
    if term.lower().endswith('s'):
        # Handles 'shirts' -> 'shirt'
        return term[:-1]
    
    # Handles terms like 'glasses' -> 'glass' or 'boxes' -> 'box'
    # This is a basic rule and won't cover irregular plurals like 'mice' or 'children'.
    return term

class ProductView(APIView):
    def get(self, request):
        name = request.query_params.get('search', None)
        
        result = Product.objects.all()

        if name:
            # 1. Get the singular root of the user's search term (e.g., 'pant' from 'longpant')
            singular_name = singularize_search_term(name)
            

            query = Q(name__icontains=name)
            
            if singular_name != name:
                query |= Q(name__icontains=singular_name)
                
            search_terms = name.split()
            
            # Add the singularized version of each word
            for term in list(search_terms):
                search_terms.append(singularize_search_term(term))
            
            final_query = Q()
            for term in set(search_terms): # Use set to avoid duplicates
                if term:
                    final_query |= Q(name__icontains=term)
            
            result = result.filter(final_query)
        
        serializer = ProductSerializer(result, many=True)
        return Response(serializer.data)



logger = logging.getLogger(__name__)

@method_decorator(csrf_exempt, name='dispatch')
class TelegramWebhookView(APIView):
    def post(self, request, *args, **kwargs):
        update = Update.de_json(request.data, BOT_APP.bot)
        future = asyncio.run_coroutine_threadsafe(BOT_APP.process_update(update), loop)
        future.result()  # wait until processed
        return JsonResponse({"ok": True})

class SetWebhookView(APIView):
    def get(self, request, *args, **kwargs):
        # NOTE: This view is SYNCHRONOUS, as setting a webhook is a simple external request.

        WEBHOOK_PATH = f"/api/webhook/{os.getenv('TELEGRAM_TOKEN')}/" # Adjust '/api/v1' to your project's root path if needed
        WEBHOOK_URL = f"{os.getenv('HOST')}{WEBHOOK_PATH}"

        TELEGRAM_API = f"https://api.telegram.org/bot{os.getenv('TELEGRAM_TOKEN')}/"
        print(TELEGRAM_API)

        # 1. DELETE any old webhook first
        try:
            requests.post(TELEGRAM_API + "deleteWebhook")
        except requests.exceptions.RequestException as e:
            logger.warning(f"Failed to delete old webhook (ok to continue): {e}")

        # 2. SET the new webhook
        try:
            response = requests.post(
                TELEGRAM_API + "setWebhook",
                data={'url': WEBHOOK_URL, 'allowed_updates': ['message', 'callback_query']}
            )
            response.raise_for_status() # Raise exception for bad status codes
            result = response.json()
        
        except requests.exceptions.RequestException as e:
            error_msg = f"Failed to set webhook. Check your URL is HTTPS: {e}"
            logger.error(error_msg)
            return Response({"status": "failed", "description": error_msg}, status=HTTPStatus.SERVICE_UNAVAILABLE)

        # 3. Return result to the user
        return Response({
            "status": "success" if result.get('ok') else "failed",
            "description": result.get('description'),
            "webhook_set_to": WEBHOOK_URL
        }, status=HTTPStatus.OK)
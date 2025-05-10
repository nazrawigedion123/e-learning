from django.shortcuts import render

# Create your views here.

from django.http import JsonResponse, HttpResponseBadRequest
import json
from .service.createOrderService import CreateOrderService # adjust import as needed
from user.permission import IsAdminOrInstructorOwner,IsClient
from rest_framework.decorators import api_view, permission_classes
from .config.config import ENV_VARIABLES

@api_view(['POST'])
@permission_classes([IsClient])
def create_order_view(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Invalid request method")

    try:
        body = json.loads(request.body)
        title = body.get("title")
        amount = body.get("amount")

        if not title or not amount:
            return JsonResponse({"error": "Title and amount are required"}, status=400)

        # Setup environment credentials (you may want to store these in settings.py)
        BASE_URL = ENV_VARIABLES["baseUrl"]  # Replace with actual URL
        fabricAppId =  ENV_VARIABLES["fabricAppId"]
        appSecret =  ENV_VARIABLES["appSecret"]
        merchantAppId =  ENV_VARIABLES["merchantAppId"]
        merchantCode =  ENV_VARIABLES["merchantCode"]

        # Create the service and call createOrder
        service = CreateOrderService(
            req={"title": title, "amount": amount},
            BASE_URL=BASE_URL,
            fabricAppId=fabricAppId,
            appSecret=appSecret,
            merchantAppId=merchantAppId,
            merchantCode=merchantCode,
        )

        raw_request = service.createOrder()

        return JsonResponse({"rawRequest": raw_request})

    except Exception as e:
        print("Error in create_order_view:", e)
        return JsonResponse({"error": str(e)}, status=500)
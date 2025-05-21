import json
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST, require_http_methods

from app import service

@require_POST
def create_secret(request):
    try:
        data = json.loads(request.body)
        message = data.get("encrypted_message")
        token = service.save_secret(message)
        data = {
            "token": token
        }
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({"error": "Failed to create secret"}, status=500)

@require_http_methods(["DELETE"])
def delete_secret(request, token):
    try:
        service.delete_secret(token)
        return HttpResponse(status=204)
    except Exception as e:
        return JsonResponse({"error": "Failed to delete secret"}, status=500)
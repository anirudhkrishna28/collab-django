from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pymongo import MongoClient
import json

# Set up MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["collabdb"]
users = db["users"]

@csrf_exempt
def register(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=405)
    try:
        data = json.loads(request.body)
        username = data.get("username", "").strip()
        password = data.get("password", "").strip()
        if not username or not password:
            return JsonResponse({"error": "Username and password required"}, status=400)
        if users.find_one({"username": username}):
            return JsonResponse({"error": "Username already exists"}, status=409)
        users.insert_one({"username": username, "password": password})
        return JsonResponse({"success": True, "username": username})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def login(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=405)
    try:
        data = json.loads(request.body)
        username = data.get("username", "").strip()
        password = data.get("password", "").strip()
        user = users.find_one({"username": username})
        if user and user.get("password") == password:
            return JsonResponse({"success": True, "username": username})
        return JsonResponse({"error": "Invalid credentials"}, status=401)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
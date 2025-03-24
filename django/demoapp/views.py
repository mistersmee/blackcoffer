from django.shortcuts import render
from django.http import JsonResponse
from .models import UserData

def index(request):
    return render(request, 'index.html')

def submit(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')

        if not name or not email:
            return JsonResponse({"error": "Name and email are required"}, status=400)

       # Store in database
        if not UserData.objects.filter(email=email).exists():
            UserData.objects.create(name=name, email=email)
            return JsonResponse({"message": "Data saved successfully!"})
        else:
            return JsonResponse({"error": "Email already exists."}, status=400)

def data_view(request):
    data = UserData.objects.all()
    return render(request, 'data.html', {'data': data})

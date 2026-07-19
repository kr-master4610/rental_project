from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from django.contrib.auth import login, get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer
from .forms import RegisterForm

User = get_user_model()

# --- API View ---
class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({"message": "User registered!", "tokens": {"refresh": str(refresh), "access": str(refresh.access_token)}}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        return Response({"id": user.id, "username": user.username, "email": user.email}, status=200)

# --- HTML View ---
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            # Назначение группы
            group_name = 'landlords' if form.cleaned_data['is_landlord'] else 'tenants'
            group, _ = Group.objects.get_or_create(name=group_name)
            user.groups.add(group)
            login(request, user)
            return redirect('/')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})
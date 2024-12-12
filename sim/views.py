import os

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from google.oauth2 import id_token
from google.auth.transport import requests, Response
from rest_framework import viewsets, status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import JobSeekers, Employer, JobListings
from .serializers import JobSeekersSerializers, EmployerSerializers, JobListingsSerializers, \
    JobSeekersSerializersProfile, EmployerSerializersProfile


class JobSeekersViewSets(viewsets.ModelViewSet):
    queryset = JobSeekers.objects.all()
    serializer_class = JobSeekersSerializers


class JobSeekersViewSetsProfile(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            job_seeker = JobSeekers.objects.get(user=request.user)
            serialzer = JobSeekersSerializersProfile(job_seeker)
            return Response(serialzer.data)
        except JobSeekers.DoesNotExist:
            return Response({'error': 'Job Seeker Profile Not Found'}, status=404)


class EmployerViewSets(viewsets.ModelViewSet):
    queryset = Employer.objects.all()
    serializer_class = EmployerSerializers


class JobListingsViewSets(viewsets.ModelViewSet):
    queryset = JobListings.objects.all()
    serializer_class = JobListingsSerializers


class RegisterAPIView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            return Response({'error', 'Username or Password are required'}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create_user(username=username, password=password)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': str(token)})


class LoginAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': str(token)})
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@csrf_exempt
def sign_in(request):
    return render(request, 'sign_in.html')


@csrf_exempt
def auth_receiver(request):
    """
    Google calls this URL after the user has signed in with their Google account.
    """
    print('Inside')
    token = request.POST['credential']

    try:
        user_data = id_token.verify_oauth2_token(
            token, requests.Request(), os.environ['GOOGLE_OAUTH_CLIENT_ID']
        )
    except ValueError:
        return HttpResponse(status=403)

    # In a real app, I'd also save any new user here to the database.
    # You could also authenticate the user here using the details from Google (https://docs.djangoproject.com/en/4.2/topics/auth/default/#how-to-log-a-user-in)
    request.session['user_data'] = user_data

    return redirect('sign_in')


def sign_out(request):
    del request.session['user_data']
    return redirect('sign_in')

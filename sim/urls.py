from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import JobSeekersViewSets, EmployerViewSets, JobListingsViewSets, RegisterAPIView, LoginAPIView, \
    JobSeekersViewSetsProfile

# API router setup
router = DefaultRouter()
router.register(r'jobseekers', JobSeekersViewSets)
router.register(r'employers', EmployerViewSets)
router.register(r'joblisting', JobListingsViewSets)

# URLs configuration
urlpatterns = [
    path('api/', include(router.urls)),  # All API endpoints
    path('', views.sign_in, name='sign_in'),  # Authentication login
    path('sign-out', views.sign_out, name='sign_out'),  # Authentication logout
    path('auth-receiver', views.auth_receiver, name='auth_receiver'),  # Auth receiver
    path('api/register', RegisterAPIView.as_view(), name='register'),
    path('api/login', LoginAPIView.as_view(), name='login'),
    path('api/jobseekers/profile', JobSeekersViewSetsProfile.as_view(), name='jobseekerprofile'),
]

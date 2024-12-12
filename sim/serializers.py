from rest_framework import serializers
from .models import JobSeekers, Employer, JobListings


class JobSeekersSerializers(serializers.ModelSerializer):
    class Meta:
        model = JobSeekers
        fields = '__all__'


class EmployerSerializers(serializers.ModelSerializer):
    class Meta:
        model = Employer
        fields = '__all__'


class JobListingsSerializers(serializers.ModelSerializer):
    class Meta:
        model = JobListings
        fields = '__all__'


class JobSeekersSerializersProfile(serializers.ModelSerializer):
    class Meta:
        model = JobSeekers
        fields = ['id', 'user', 'bio', 'resume']


class EmployerSerializersProfile(serializers.ModelSerializer):
    class Meta:
        model = Employer
        fields = ['id', 'user', 'company_name', 'company_website']

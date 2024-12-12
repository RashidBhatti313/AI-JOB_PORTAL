from django.db import models


# Create your models here.
class JobSeekers(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    resume = models.FileField(upload_to='resume/')

    def __str__(self):
        return self.name


class Employer(models.Model):
    company_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.company_name


class JobListings(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)
    posted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

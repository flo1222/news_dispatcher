from django.db import models

# Create your models here.

class Site(models.Model):
    name = models.CharField(max_length=200)
    siret_number = models.CharField(max_length=20, null=True, blank=True)

class Article(models.Model):
    url = models.CharField(max_length=300)
    image_url = models.CharField(max_length=400, null=True, blank=True)
    description = models.CharField(max_length=1000, null=True, blank=True)
    source = models.CharField(max_length=50, null=True, blank=True)
    pub_date = models.DateField(null=True, blank=True) 
    industrial_site = models.ForeignKey(Site, models.SET_NULL, null=True, blank=True)
    def __str__(self):          
        return f"News#{self.id}" 

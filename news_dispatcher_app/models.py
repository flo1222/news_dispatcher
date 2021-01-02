from django.db import models

# Create your models here.

class Site(models.Model):
    name = models.CharField(max_length=200)
    usual_name = models.CharField(max_length=200, null=True, blank=True)
    siret_number = models.CharField(max_length=20, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    company = models.CharField(max_length=200, null=True, blank=True)
    matche_count = models.IntegerField(null=True, blank=True, default=0)

class Article(models.Model):
    url = models.CharField(max_length=300)
    image_url = models.CharField(max_length=400, null=True, blank=True)
    title = models.CharField(max_length=400, null=True, blank=True)
    description = models.CharField(max_length=1000, null=True, blank=True)
    source = models.CharField(max_length=50, null=True, blank=True)
    pub_date = models.DateField(null=True, blank=True) 
    industrial_site = models.ForeignKey(Site, models.SET_NULL, null=True, blank=True)
    def __str__(self):          
        return f"News#{self.id}" 

class F3_Article(models.Model):
    url = models.CharField(max_length=300)
    image_url = models.CharField(max_length=400, null=True, blank=True)
    title = models.CharField(max_length=400, null=True, blank=True)
    description = models.CharField(max_length=1000, null=True, blank=True)
    full_text = models.CharField(max_length=5000, null=True, blank=True)
    text_english = models.CharField(max_length=5000, null=True, blank=True)
    source = models.CharField(max_length=50, null=True, blank=True)
    pub_date = models.DateField(null=True, blank=True) 
    industrial_site = models.ForeignKey(Site, models.SET_NULL, null=True, blank=True)
    relevant = models.BooleanField(null=True, blank=True)
    is_industrial = models.BooleanField(null=True, blank=True)
    sorted_industrial = models.BooleanField(default=False, blank=True)
    
    def __str__(self):          
        return f"News#{self.id}" 
    
    def check_for_duplicates(self):
        count = 0
        if F3_Article.objects.filter(url=self.url).count() > 1:
            self.delete()
            print('row deleted = ')
        return None
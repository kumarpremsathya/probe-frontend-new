from django.db import models

# Create your models here.
class city(models.Model):
    table_name= models.CharField(max_length=55)
    status=models.CharField(max_length=30)
    data_scraped= models.IntegerField()
    reason= models.CharField(max_length=100)
    scraped_at = models.DateField(null=True, blank=True)
       
    class Meta:
        db_table = "city"
    
class base(models.Model):
    Name= models.CharField(max_length=55)
    CountryCode=models.CharField(max_length=30)
    Population= models.IntegerField()
    
    class Meta:
        db_table = "base"
    

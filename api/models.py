from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from api.constants import MONTH_CHOICES,SEASON_CHOICES

class Region(models.Model):
    name = models.CharField(max_length=50,unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering =["name"]


class Unit(models.Model):
    name = models.CharField(max_length=20,unique=True)

    def __str__(self):
        return self.name
    
class Parameter(models.Model):
    name = models.CharField(max_length=50,unique=True)
    unit = models.ForeignKey(Unit,on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} - {self.unit}'
    
    class Meta:
        ordering = ["name"]


class WeatherData(models.Model):
    year = models.IntegerField(validators=[MinValueValidator(1000),MaxValueValidator(9999)],null=False)
    region = models.ForeignKey(Region,on_delete=models.CASCADE,related_name='%(class)s',null=False)
    parameter = models.ForeignKey(Parameter,on_delete=models.CASCADE,related_name='%(class)s',null=False)
    value = models.FloatField()

    class Meta:
        abstract = True
        ordering=["year"]


class MonthlyData(WeatherData):
    
    month=models.CharField(max_length=100,choices=MONTH_CHOICES,null=False)
   
    def __str__(self):
        return f'{self.year} - {self.month}'
    
    class Meta:
        unique_together=["year","region","month","parameter","value"]

  
    
class SeasonalData(WeatherData):
    
    season=models.CharField(max_length=50,choices=SEASON_CHOICES,null=False)
   
    def __str__(self):
        return f'{self.year} - {self.season}'
    
    class Meta:
        unique_together=["year","region","season","parameter","value"]
    
    
class AnnualData(WeatherData):
   
   
   def __str__(self):
       return f'{self.year} - {self.region}'
   
   class Meta:
        unique_together=["year","season","parameter","value"]
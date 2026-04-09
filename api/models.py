from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from api.constants import MONTH_CHOICES,SEASON_CHOICES,UNIT_CHOICES


class Year(models.Model):
    year = models.IntegerField(validators=[MinValueValidator(1000),MaxValueValidator(9999)],null=False)

class Region(models.Model):
    name = models.CharField(max_length=50,unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering =["name"]


class Unit(models.Model):
    name = models.CharField(max_length=20,unique=True,choices=UNIT_CHOICES)

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
    year = models.ForeignKey(Year,on_delete=models.CASCADE,null=False,related_name='%(class)s')
    region = models.ForeignKey(Region,on_delete=models.CASCADE,null=False,related_name='%(class)s')
    parameter = models.ForeignKey(Parameter,on_delete=models.CASCADE,null=False,related_name='%(class)s')
    value = models.FloatField(null=False)

    class Meta:
        abstract = True
        ordering=["-year"]
        


class MonthlyData(WeatherData):
    
    month=models.CharField(max_length=100,choices=MONTH_CHOICES,null=False)
   
    def __str__(self):
        return f'{self.year} - {self.month} - {self.region} - {self.parameter} - {self.value}'
    
    class Meta:
       ordering=["-year"]
       constraints = [
            models.UniqueConstraint(
                fields=["year","region","parameter","month"],
                name="unique_monthly_data"
            )
        ]
       indexes =[models.Index(fields=['year','region','parameter','month'],name='monthly_data_idx')]

  
    
class SeasonalData(WeatherData):
    
    season=models.CharField(max_length=50,choices=SEASON_CHOICES,null=False)
   
    def __str__(self):
        return f'{self.year} - {self.season} - {self.region} - {self.parameter} - {self.value}'
    
    class Meta:
        ordering=["-year"]
        constraints = [
            models.UniqueConstraint(
                fields=["year","region","parameter","season"],
                name="unique_seasonal_data"
            )
        ]
        indexes =[models.Index(fields=['year','region','parameter','season'],name='seasonal_data_idx')]

    
    
class AnnualData(WeatherData):
   
   
   def __str__(self):
       return f'{self.year} - {self.region} - {self.parameter} - {self.value}'
   
   class Meta:
        ordering=["-year"]
        constraints = [
            models.UniqueConstraint(
                fields=["year","region","parameter"],
                name="unique_annual_data"
            )
        ]
        indexes =[models.Index(fields=['year','region','parameter'],name='annual_data_idx')]

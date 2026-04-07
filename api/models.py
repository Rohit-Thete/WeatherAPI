from django.db import models

class Region(models.Model):
    name = models.CharField(max_length=50,unique=True)

    def __str__(self):
        return self.name
    
class Parameter(models.Model):
    name =models.CharField(max_length=50,unique=True)
    unit = models.CharField(max_length=10,unique=True)

    def __str__(self):
        return f'{self.name} - {self.unit}'


class WeatherData(models.Model):
    year = models.IntegerField()
    region = models.ForeignKey(Region,on_delete=models.CASCADE,name='regions')
    parameter = models.ForeignKey(Parameter,on_delete=models.CASCADE,name='parameters')
    value = models.FloatField(default="")

    class Meta:
        abstract = True
        ordering=["year"]


class MonthlyData(WeatherData):
    MONTH_CHOICES =[
        (1,"January"),(2,"February"),(3,"March"),
        (4,"April"),(5,"May"),(6,"June"),
        (7,"July"),(8,"August"),(9,"September"),
        (10,"October"),(11,"November"),(12,"December")]
    month=models.CharField(max_length=100,choices=MONTH_CHOICES)
   
    def __str__(self):
        return f'{self.year} - {self.month}'
    
    class Meta:
        unique_together=["year","region","month","parameter","value"]

  
    
class SeasonalData(WeatherData):
    SEASON_CHOICES=[("Winter","Winter"),("Spring","Spring"),("Summer","Summer"),("Autumn","Autumn")]
    season=models.CharField(max_length=50,choices=SEASON_CHOICES)
   
    def __str__(self):
        return f'{self.year} - {self.season}'
    
    class Meta:
        unique_together=["year","region","season","parameter","value"]
    
    
class AnnualData(WeatherData):
   
   
   def __str__(self):
       return f'{self.year} - {self.region}'
   
   class Meta:
        unique_together=["year","season","parameter","value"]

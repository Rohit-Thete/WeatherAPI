from django.db import models

class MonthlyData(models.Model):
    year=models.IntegerField()
    month=models.CharField(max_length=100)
    region=models.CharField(max_length=50)
    parameter=models.CharField(max_length=50)
    temprature=models.FloatField(null=True)
    

    def __str__(self):
        return f'{self.year} - {self.month}'
    
class SeasonalData(models.Model):
    year=models.IntegerField()
    season=models.CharField(max_length=50)
    region=models.CharField(max_length=50)
    parameter=models.CharField(max_length=50)
    temprature=models.FloatField(null=True)

    def __str__(self):
        return f'{self.year} - {self.season}'
    
class AnnualData(models.Model):
    year=models.IntegerField()
    region=models.CharField(max_length=50)
    parameter=models.CharField(max_length=50)
    temprature=models.FloatField(null=True)

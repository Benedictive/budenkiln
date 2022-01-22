from django.db import models

class TemperatureCurve(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name 

class TemperaturePoint(models.Model):
    # With cascade the points are deleted if the curve is deleted.
    curve = models.ForeignKey(TemperatureCurve, on_delete=models.CASCADE)
    # the x-coordinate of our point in minutes
    time = models.PositiveIntegerField()
    # the y-coordinate of our point in degrees celcious
    temperature = models.PositiveIntegerField() 

    def __str__(self):
        return f'{self.time}:{self.temperature}'
   
class Kiln(models.Model):
    last_curve = models.ForeignKey(TemperatureCurve, on_delete=models.CASCADE)
    
    def __str__(self):
        return "THERE WILL BE NO MERCY FOR THOSE WHO HAVE NOT SHOWN MERCY TO THE ALMIGHTY KILN"

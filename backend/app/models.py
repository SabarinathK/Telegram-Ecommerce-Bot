from django.db import models

# Create your models here.
class products(models.Model):
    name=models.CharField(max_length=100)
    image=models.ImageField(null=True,blank=True)
    description=models.TextField()
    price=models.FloatField()

    def __str__(self):
        return self.name
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField(null=True, blank=True)
    price = models.FloatField()
    stock = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f'{self.id}| {self.name}'

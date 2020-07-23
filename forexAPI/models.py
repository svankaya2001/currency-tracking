from django.db import models

# Create your models here.

class Currency(models.Model):
    name = models.CharField(max_length = 20)
    price = models.CharField(max_length = 20)
    change_p = models.CharField(max_length = 20)
    M_cap = models.CharField(max_length = 20)
    supply = models.CharField(max_length = 20)
    volume = models.CharField(max_length = 20)

    class Meta:
        verbose_name = 'Currency'
        verbose_name_plural = 'Currencies'
    
    def __str__(self):
        return self.pair

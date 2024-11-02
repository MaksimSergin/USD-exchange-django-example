from django.db import models

class ExchangeRate(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    rate = models.DecimalField(max_digits=10, decimal_places=4)

    def __str__(self):
        return f"Rate at {self.timestamp}: {self.rate}"

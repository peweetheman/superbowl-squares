from django.db import models

class TakenSquare(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    display_name = models.CharField(max_length=255)
    row = models.IntegerField()
    column = models.IntegerField()

    def __str__(self):
        return f"{self.first_name} {self.last_name} - Square ({self.row}, {self.column})"

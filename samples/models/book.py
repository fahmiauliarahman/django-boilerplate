from django.db import models


class Book(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(max_length=255)
    photo = models.ImageField(upload_to="books", null=True, blank=True, default=None)
    published_date = models.DateField()
    is_released = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

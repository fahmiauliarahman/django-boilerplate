import random
import string

from django.db import models
from django.utils.text import slugify


class Book(models.Model):
    def __str__(self):
        return self.name

    def upload_path(instance, filename):
        ext = filename.split(".")[-1]
        # we will assign the uploaded file to a random name
        random_string = "".join(
            [random.choice(string.ascii_letters) for _ in range(10)]
        )
        filename = "{random_string}.{ext}".format(random_string=random_string, ext=ext)

        return "books/{filename}".format(filename=filename)

    # override save method
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)
    photo = models.ImageField(
        upload_to=upload_path, null=True, blank=True, default=None
    )
    published_date = models.DateField()
    is_released = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

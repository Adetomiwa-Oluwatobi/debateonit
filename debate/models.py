from django.db import models

# Create your models here.
# debate/models.py


class Topic(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

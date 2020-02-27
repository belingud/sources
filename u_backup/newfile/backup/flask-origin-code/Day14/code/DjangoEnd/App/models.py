from django.db import models
from tinymce.models import HTMLField


class Blog(models.Model):
    b_title = models.CharField(max_length=32)
    b_content = HTMLField()

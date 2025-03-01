from django.db import models

class user_text(models.Model):
    creation_time = models.DateTimeField()
    user_ip = models.GenericIPAddressField()
    user_name = models.TextField()
    rating = models.IntegerField()
    text = models.TextField()
    text_name = models.TextField()

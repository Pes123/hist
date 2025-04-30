from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg
from django.db.models.signals import post_save
from django.dispatch import receiver

class user_text(models.Model):
    creation_time = models.DateTimeField(auto_now_add=True)
    user_ip = models.GenericIPAddressField()
    user_name = models.TextField()
    text = models.TextField()
    text_name = models.TextField()
    rating = models.FloatField(default=0)  # Поле для хранения среднего рейтинга

    def update_rating(self):
        # Обновляем рейтинг в поле модели UserText
        average_rating = UserRating.objects.filter(text=self).aggregate(Avg('rating'))['rating__avg'] or 0
        self.rating = average_rating
        self.save()

class UserRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.ForeignKey(user_text, on_delete=models.CASCADE, related_name='ratings')
    rating = models.FloatField()

    class Meta:
        unique_together = ('user', 'text')  # Уникальность для пользователя и текста

@receiver(post_save, sender=UserRating)
def update_user_text_rating(sender, instance, **kwargs):
    # Обновляем рейтинг текста после сохранения UserRating
    instance.text.update_rating()

from django.contrib import admin
from django.urls import path, include
from myproject.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name="home"),  # Указываем домашнюю страницу
    path('posts/', include("post_and_show.urls")),  # Подключаем URL конфигурацию приложения "post_and_show"
]
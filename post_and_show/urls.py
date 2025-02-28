from django.urls import path
from .views import text_entry_view, text_list, text_special


app_name = 'posts'

urlpatterns = [
    path('texts/', text_list, name='text_list'),
    path('text-entry/', text_entry_view, name='text_entry'),
    path("text-special/", text_special, name='text_special')
]
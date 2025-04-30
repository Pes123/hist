from django.urls import path
from .views import submit_rating, text_entry_view, text_list, text_list_autor, text_special


app_name = 'posts'

urlpatterns = [
    path('texts/', text_list, name='text_list'),
    path("texts_a/", text_list_autor, name='text_list_autor'),
    path('text-entry/', text_entry_view, name='text_entry'),
    path("text-special/", text_special, name='text_special'),
    path('submit_rating/', submit_rating, name='submit_rating'),
]
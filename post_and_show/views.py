from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from .forms import TextEntryForm
from .models import UserRating, user_text
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Avg

@login_required
def text_list_autor(request):
    sort_order = request.GET.get('sort', 'asc')  
    sort_by = request.GET.get('by', 'rating')  

    texts = user_text.objects.all()

    if sort_by == 'date':
        texts = texts.order_by('-creation_time' if sort_order == 'desc' else 'creation_time') 
    else:  
        texts = texts.order_by('-rating' if sort_order == 'desc' else 'rating')

    paginator = Paginator(texts, 5)  
    page_number = request.GET.get('page')  
    page_obj = paginator.get_page(page_number)  

    # Получаем рейтинги для авторизованного пользователя
    user_ratings = UserRating.objects.filter(user=request.user).values('text_id', 'rating')

    return render(request, 'text_list_autor.html', {
        'page_obj': page_obj,
        'sort_order': sort_order,
        'sort_by': sort_by,
        'user_ratings': {rating['text_id']: rating['rating'] for rating in user_ratings},
    })


@csrf_exempt
@login_required


def submit_rating(request):
    if request.method == "POST":
        text_id = request.POST.get('text_id')  # ID текста
        rating = request.POST.get('rating')  # Новый рейтинг

        user_text_instance = get_object_or_404(user_text, id=text_id)

        if rating is not None:
            # Преобразуем рейтинг в число с плавающей запятой
            rating = float(rating)

            # Обновляем или создаем рейтинг для текущего пользователя
            UserRating.objects.update_or_create(
                user=request.user, 
                text=user_text_instance,
                defaults={'rating': rating}
            )

            # Теперь вычисляем средний рейтинг
            average_rating = UserRating.objects.filter(text=user_text_instance).aggregate(Avg('rating'))['rating__avg']
            average_rating = average_rating if average_rating is not None else 0  # Если нет оценок, возвращаем 0

            return JsonResponse({
                'status': 'success',
                'new_rating': rating,
                'average_rating': average_rating
            })

        return JsonResponse({'status': 'error', 'error': 'Недостаточно данных'})

    return JsonResponse({'status': 'error', 'error': 'Неверный метод'})



def text_list(request):
    sort_order = request.GET.get('sort', 'asc')  
    sort_by = request.GET.get('by', 'rating')  

    texts = user_text.objects.all()

   
    if sort_by == 'date':
        texts = texts.order_by('-creation_time' if sort_order == 'desc' else 'creation_time') 
    else:  
        texts = texts.order_by('-rating' if sort_order == 'desc' else 'rating')

    paginator = Paginator(texts, 5)  
    page_number = request.GET.get('page')  
    page_obj = paginator.get_page(page_number)  

    return render(request, 'text_list.html', {'page_obj': page_obj, 'sort_order': sort_order, 'sort_by': sort_by})


def text_special(request):
    selected_ids = [8]  
    texts = user_text.objects.filter(id__in=selected_ids)

    paginator = Paginator(texts, 3) 
    page_number = request.GET.get('page')  
    page_obj = paginator.get_page(page_number)  

    return render(request, 'text_special.html', {'page_obj': page_obj})

def text_entry_view(request):
    form = TextEntryForm()  
    if request.method == 'POST':
        form = TextEntryForm(request.POST)  
        if form.is_valid():
            text_entry = form.save(commit=False)
            text_entry.user_ip = get_client_ip(request)
            text_entry.creation_time = timezone.now()
            text_entry.rating = 0
            text_entry.save()
            
    return render(request, 'text_entry.html', {'form': form})

def get_client_ip(request):
    """Получение IP-адреса пользователя"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
from django.shortcuts import render, redirect
from .forms import TextEntryForm
from .models import user_text
from django.utils import timezone
from django.core.paginator import Paginator




def text_list(request):
    sort_order = request.GET.get('sort', 'asc')  # Параметр сортировки
    sort_by = request.GET.get('by', 'rating')  # Параметр выбора сортировки

    texts = user_text.objects.all()

    # Сортировка по рейтингу или дате
    if sort_by == 'date':
        texts = texts.order_by('-creation_time' if sort_order == 'desc' else 'creation_time')  # По дате создания
    else:  # По рейтингу по умолчанию
        texts = texts.order_by('-rating' if sort_order == 'desc' else 'rating')

    paginator = Paginator(texts, 5)  # Пагинация: 3 текста на страницу
    page_number = request.GET.get('page')  # Получаем номер страницы
    page_obj = paginator.get_page(page_number)  # Получаем текст для текущей страницы

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
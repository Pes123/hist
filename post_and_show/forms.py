from django import forms
from .models import user_text  

class TextEntryForm(forms.ModelForm):
    class Meta:
        model = user_text
        fields = ['user_name','text_name', 'text']
        widgets = {
            'user_name': forms.TextInput(attrs={
                'placeholder': 'Введите ваше ФИО',
                'class': 'form-control custom-textarea',
                'style': 'resize: none; border: 1px solid #ccc; padding: 10px;',  
            }),
            'text_name': forms.TextInput(attrs={
                'placeholder': 'Введите название текста',
                'class': 'form-control custom-textarea',
                'style': 'resize: none; border: 1px solid #ccc; padding: 10px;',  
            }),
            'text': forms.Textarea(attrs={
                'placeholder': 'Введите текст...',
                'class': 'form-control custom-textarea',
                'rows': 20,
                'cols': 40,
                'style': 'resize: none; border: 1px solid #ccc; padding: 10px;',
            }),



        }

    def __init__(self, *args, **kwargs):
        super(TextEntryForm, self).__init__(*args, **kwargs)
        self.fields['user_name'].label = ''
        self.fields['text_name'].label = ''
        self.fields['text'].label = ''


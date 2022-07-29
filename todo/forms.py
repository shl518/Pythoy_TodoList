from django.forms import ModelForm
from .models import Todo


# Todo Form
class TodoForm(ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'memo', 'expiration_date', 'level', 'everyday']

from django.forms import ModelForm
from .models import Todo


# Todo Form
class TodoForm(ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'memo', 'expiration_date', 'level', 'predict_hour', 'predict_minute', 'isDaily', 'tag',
                  'fixedTime_end', 'fixedTime_start']

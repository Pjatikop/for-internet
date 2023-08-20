from django.forms import ModelForm
from .models import Radio


class RadioForm(ModelForm):
    class Meta:
        model = Radio
        fields = ['title', 'demo_link', 'name_link']
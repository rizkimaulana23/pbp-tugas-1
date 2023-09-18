from django.forms import ModelForm
from main.models import Oculi

class ProductForm(ModelForm):
    class Meta:
        model = Oculi
        fields = ["name", "region", "amount_collected", "amount", "description"]
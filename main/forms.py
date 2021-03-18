from django import forms

from .models import Order



class OrderForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ordered_at'].label = 'Дата получения заказа'
        self.fields['address'].label = 'Адрес'

    ordered_at = forms.DateField(widget=forms.TextInput({'type': 'date'}))

    class Meta:
        model = Order
        fields = (
            'first_name', 'last_name', 'phone', 'address', 'buying_type', 'ordered_at', 'comment'
        )






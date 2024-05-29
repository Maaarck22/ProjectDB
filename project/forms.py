from django import forms
from .models import Products, Category

class ProductForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['Product_name', 'Description', 'Price', 'Availability', 'Image', 'Category']
        widgets = {
            'Category': forms.Select(attrs={'class': 'form-control'}),
        }
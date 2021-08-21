from django.forms import ModelForm

class ProductForm(ModelForm):
    class Meta:
        model=Product
        fields = ['product_category']


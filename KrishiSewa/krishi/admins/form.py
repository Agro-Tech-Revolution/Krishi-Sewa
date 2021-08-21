from django.forms import ModelForm
from farmers.models import Product

class ProductCategoryForm(ModelForm):
    class Meta:
        model=Product
        fields = ['prod_name', 'prod_categories', 'prod_img']
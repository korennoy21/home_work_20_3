from django import forms

from catalog.models import Product, Category, Version



NULLABLE = {'blank': True, 'null': True}


class MyCleanForm:
    WORDS = (
        'казино', 'криптовалюта', 'крипта',
        'биржа', 'дешево', 'бесплатно',
        'обман', 'полиция', 'радар'
    )

    def clean_name(self):
        cleaned_data = self.cleaned_data.get('name').lower()
        for word in self.WORDS:
            if word in cleaned_data:
                raise forms.ValidationError('Ошибка!Данные слова запрещены')
        return cleaned_data

    def clean_description(self):
        cleaned_data = self.cleaned_data.get('description').lower()
        for word in self.WORDS:
            if word in cleaned_data:
                raise forms.ValidationError('Ошибка!Данные слова запрещены')
        return cleaned_data

    def clean_title(self):
        cleaned_data = self.cleaned_data.get('title').lower()
        for word in self.WORDS:
            if word in cleaned_data:
                raise forms.ValidationError('Ошибка!Данные слова запрещены')
        return cleaned_data


class CustomFormMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class ProductForm(CustomFormMixin, MyCleanForm, forms.ModelForm):

    class Meta:
        model = Product
        fields = '__all__'


class CategoryForm(CustomFormMixin, MyCleanForm, forms.ModelForm):
    """Форма создания и редактирования категории"""

    class Meta:
        model = Category
        fields = '__all__'


class VersionForm(CustomFormMixin, MyCleanForm, forms.ModelForm):
    """Форма создания и редактирования версии продукта"""

    class Meta:
        model = Version
        fields = '__all__'

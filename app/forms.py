from django import forms
from .models import Review
from .models import Address
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from django_countries import countries
from django_countries.widgets import CountrySelectWidget
from django_countries.fields import CountryField
from django.contrib.auth.forms import PasswordResetForm as DjangoPasswordResetForm
from django.contrib.auth.models import User


class PasswordResetForm(DjangoPasswordResetForm):
    email = forms.EmailField(label='', max_length=254, widget=forms.EmailInput(attrs={'autocomplete': 'email', 'class': 'form-control', 'placeholder': 'Indirizzo email'}))

    def clean_email(self):
        """
        Verifica che l'email fornita corrisponda a un utente esistente
        """
        email = self.cleaned_data['email']
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            raise forms.ValidationError("Non esiste alcun utente associato a questa email.")
        return email


class PaymentForm(forms.Form):
    amount = forms.DecimalField(max_digits=8, decimal_places=2)
    payment_method = forms.ChoiceField(choices=[('bank_transfer', 'Bank Transfer'), ('credit_card', 'Credit Card')])

class AddressForm(forms.ModelForm):
    country = CountryField().formfield(widget=CountrySelectWidget(attrs={
        'class': 'form-select form-control'
    }))

    class Meta:
        model = Address
        fields = ['first_name', 'last_name', 'email', 'phone', 'street_address', 'city', 'state', 'zip_code', 'country']
        widgets = {
            'phone': PhoneNumberPrefixWidget(),
            'zip_code': forms.TextInput(attrs={'type': 'number'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Phone Number', 'class': 'form-control'}),
            'street_address': forms.TextInput(attrs={'placeholder': '1234 Main St', 'class': 'form-control'}),
            'city': forms.TextInput(attrs={'placeholder': 'City', 'class': 'form-control'}),
            'state': forms.TextInput(attrs={'placeholder': 'State/Province', 'class': 'form-control'}),
            'zip_code': forms.TextInput(attrs={'placeholder': 'Zip/Postal Code', 'class': 'form-control'}),
        }
        labels = {
            'first_name': '',
            'last_name': '',
            'email': '',
            'phone': '',
            'street_address': '',
            'city': '',
            'state': '',
            'zip_code': '',
            'country': '',
        }
        error_messages = {
            'zip_code': {'invalid': 'Please enter a valid zip code.'},
        }

class ReviewForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    rating = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    author_image = forms.ImageField(widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))

    class Meta:
        model = Review
        fields = ['name', 'rating', 'author_image', 'message']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) < 2:
            raise forms.ValidationError("Il nome deve essere lungo almeno 2 caratteri.")
        return name

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating < 1 or rating > 5:
            raise forms.ValidationError("Il rating deve essere compreso tra 1 e 5.")
        return rating

    def clean_message(self):
        message = self.cleaned_data.get('message')
        if len(message) < 10:
            raise forms.ValidationError("Il messaggio deve essere lungo almeno 10 caratteri.")
        return message


class ProductSearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder': 'Search your Product'}))
    
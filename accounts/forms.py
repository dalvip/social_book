from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django import forms
from .models import UploadFile
from django import forms
from django.contrib.auth import get_user_model
from .models import Book


class RegisterForm(UserCreationForm):
    role = forms.ChoiceField(choices=CustomUser.USER_ROLES, required=True)
    class Meta:
        model = CustomUser
        fields = ['role','username', 'email', 'birth_year', 'address', 'public_visibility', 'password1', 'password2']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        
class UploadFileForm(forms.ModelForm):
    class Meta:
        model = UploadFile
        fields = ['title', 'description', 'file', 'cost', 'year_of_publication', 'visibility']

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your username'
        })
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password'
        })
    )

    User = get_user_model()

class BookForm(forms.ModelForm):
     class Meta:
        model = Book
        fields = ['title','author', 'cover_image', 'description','price','is_public','genre']
        widgets = {
            'publication_date': forms.DateInput(attrs={'type': 'date'}),
        }

class AuthorProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'address', 
                 'birth_year', 'public_visibility']
        widgets = {
            'birth_year': forms.NumberInput(attrs={'min': 1900, 'max': 2024}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Client


class MedicalEditForm(forms.ModelForm):
    phone_suffix = forms.CharField(
        max_length=8,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': '12345678',
            'pattern': '[0-9]{8}',
            'title': 'Enter 8 digits after +2519',
            'class': 'flex-1 min-w-0 px-4 py-3 border border-gray-300 rounded-r-lg focus:ring-2 focus:ring-nova-green focus:border-transparent transition-all duration-300'
        })
    )
    
    class Meta:
        model = Client
        fields = ['first_name', 'last_name', 'age', 'email', 'gender', 'diagnosis', 'treatment_plan', 'prescriptions', 'doctor_notes']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-nova-green focus:border-transparent transition-all duration-300',
                'placeholder': 'Enter first name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-nova-green focus:border-transparent transition-all duration-300',
                'placeholder': 'Enter last name'
            }),
            'age': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-nova-green focus:border-transparent transition-all duration-300',
                'placeholder': 'Enter age',
                'min': '1',
                'max': '120'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-nova-green focus:border-transparent transition-all duration-300',
                'placeholder': 'email@example.com'
            }),
            'gender': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-nova-green focus:border-transparent transition-all duration-300'
            }),
            'diagnosis': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border-l-4 border-blue-500 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-300 bg-blue-50',
                'placeholder': 'Enter medical diagnosis and findings...',
                'rows': 4
            }),
            'treatment_plan': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border-l-4 border-green-500 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all duration-300 bg-green-50',
                'placeholder': 'Describe the treatment plan and procedures...',
                'rows': 4
            }),
            'prescriptions': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border-l-4 border-purple-500 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-300 bg-purple-50',
                'placeholder': 'List prescribed medications and dosages...',
                'rows': 4
            }),
            'doctor_notes': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border-l-4 border-orange-500 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all duration-300 bg-orange-50',
                'placeholder': 'Additional observations and follow-up notes...',
                'rows': 4
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('phone', None)
        
        if self.instance and self.instance.phone:
            phone_number = self.instance.phone
            if phone_number.startswith('+2519') and len(phone_number) == 13:
                self.fields['phone_suffix'].initial = phone_number[5:]
    
    def clean_phone_suffix(self):
        phone_suffix = self.cleaned_data.get('phone_suffix')
        if not phone_suffix:
            raise forms.ValidationError("Phone number is required")
        if len(phone_suffix) != 8:
            raise forms.ValidationError("Please enter exactly 8 digits")
        if not phone_suffix.isdigit():
            raise forms.ValidationError("Phone number must contain only digits")
        return phone_suffix
    
    def save(self, commit=True):
        client = super().save(commit=False)
        phone_suffix = self.cleaned_data.get('phone_suffix')
        client.phone = f"+2519{phone_suffix}"
        if commit:
            client.save()
        return client
    
    def clean_phone_suffix(self):
        phone_suffix = self.cleaned_data.get('phone_suffix')
        if not phone_suffix:
            raise forms.ValidationError("Phone number is required")
        if len(phone_suffix) != 8:
            raise forms.ValidationError("Please enter exactly 8 digits")
        if not phone_suffix.isdigit():
            raise forms.ValidationError("Phone number must contain only digits")
        return phone_suffix
    
    def save(self, commit=True):
        client = super().save(commit=False)
        phone_suffix = self.cleaned_data.get('phone_suffix')
        client.phone = f"+2519{phone_suffix}"
        if commit:
            client.save()
        return client

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['first_name', 'last_name', 'age', 'email', 'gender', 'phone']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-nova-green focus:border-transparent transition-all duration-300',
                'placeholder': 'Enter first name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-nova-green focus:border-transparent transition-all duration-300',
                'placeholder': 'Enter last name'
            }),
            'age': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-nova-green focus:border-transparent transition-all duration-300',
                'placeholder': 'Enter age',
                'min': '1',
                'max': '120'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-nova-green focus:border-transparent transition-all duration-300',
                'placeholder': 'email@example.com'
            }),
            'gender': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-nova-green focus:border-transparent transition-all duration-300'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-nova-green focus:border-transparent transition-all duration-300',
                'placeholder': '+251912345678',
                'pattern': '\\+2519[0-9]{8}',
                'title': 'Format: +251912345678'
            }),
        }
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone.startswith('+2519'):
            raise forms.ValidationError("Phone number must start with +2519")
        if len(phone) != 13:
            raise forms.validationError("Phone number must be 13 characters (e.g., +251912345678)")
        return phone
    
    def clean_phone_suffix(self):
        phone_suffix = self.cleaned_data.get('phone_suffix')
        if not phone_suffix:
            raise forms.ValidationError("Phone number is required")
        if len(phone_suffix) != 8:
            raise forms.ValidationError("Please enter exactly 8 digits")
        if not phone_suffix.isdigit():
            raise forms.ValidationError("Phone number must contain only digits")
        return phone_suffix
    
    def save(self, commit=True):
        client = super().save(commit=False)
        phone_suffix = self.cleaned_data.get('phone_suffix')
        client.phone = f"+2519{phone_suffix}"
        if commit:
            client.save()
        return client

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(
        max_length=20, 
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': '+2519',
            'pattern': '\\+2519[0-9]{8}',
            'title': 'Phone number must start with +2519 and have 8 more digits'
        })
    )
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone', 'user_type', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_type'].required = True
        self.fields['user_type'].choices = [
            ('receptionist', 'Receptionist'),
        ]
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone and not phone.startswith('+2519'):
            raise forms.ValidationError("Phone number must start with +2519")
        if phone and len(phone) != 13:  # +2519 + 8 digits = 13 characters
            raise forms.ValidationError("Phone number must be 13 characters including +2519")
        return phone
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.phone = self.cleaned_data['phone']
        user.user_type = self.cleaned_data['user_type']
        if commit:
            user.save()
        return user

class ClientForm(forms.ModelForm):
    phone = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'placeholder': '+2519',
            'pattern': '\\+2519[0-9]{8}',
            'title': 'Phone number must start with +2519 and have 8 more digits'
        })
    )
    
    class Meta:
        model = Client
        fields = ['first_name', 'last_name', 'age', 'email', 'phone', 'gender']
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone.startswith('+2519'):
            raise forms.ValidationError("Phone number must start with +2519")
        if len(phone) != 13:  # +2519 + 8 digits = 13 characters
            raise forms.ValidationError("Phone number must be 13 characters including +2519")
        return phone
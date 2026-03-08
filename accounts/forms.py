from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserRegistrationForm(UserCreationForm):
    real_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    profile_photo = forms.ImageField(required=False)
    
    #determine roles
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    ]
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.RadioSelect)

    class Meta(UserCreationForm.Meta):
        model = User
        #fields that will show on the html page
        fields = UserCreationForm.Meta.fields + ('real_name', 'email', 'profile_photo', 'role')

    def save(self, commit=True):
        #save info
        user = super().save(commit=False)
        
        #set the correct 'switch' in database
        role = self.cleaned_data.get('role')
        if role == 'student':
            user.is_student = True
        elif role == 'teacher':
            user.is_teacher = True
            
        user.real_name = self.cleaned_data.get('real_name')
        user.profile_photo = self.cleaned_data.get('profile_photo')
        
        if commit:
            user.save() #save and push all data to database
        return user
from statistics import mode
from django import forms
from matplotlib.pyplot import cla
from .models import User


class userSignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username","email","password",)

    #username validation
    def clean_username(self):
        username = self.cleaned_data.get('username')
        model = self.Meta.model
        user = model.objects.filter(username__iexact=username) #checking input username 
        if user.exists():
            raise forms.ValidationError("Username already exists")
        return self.cleaned_data.get('username')
        
    #email validation
    def clean_email(self):
        email = self.cleaned_data.get('email')
        model = self.Meta.model
        user = model.objects.filter(email__iexact=email) #checking input email 
        if user.exists():
            raise forms.ValidationError("Email already exists")
        return self.cleaned_data.get('email')

    #password check
    def clean_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.data.get('confirm_password')
        if password!=confirm_password:
            raise forms.ValidationError ("Password not matching")
        
        return self.cleaned_data.get('password')

#Login Form
class loginForm(forms.Form):
    username = forms.CharField(max_length=250,required=True)
    password = forms.CharField(max_length=250,required=True,widget=forms.PasswordInput)
    
#Profile_Update
class UserProfileUpdateForm(forms.ModelForm):
    def _init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email", )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        model = self.Meta.model
        user = model.objects.filter(username__iexact=username).exclude(pk=self.instance.pk) #checking duplicate entry
        
        if user.exists():
            raise forms.ValidationError("A user with that name already exists")
        
        return self.cleaned_data.get('username')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        model = self.Meta.model
        user = model.objects.filter(email__iexact=email).exclude(pk=self.instance.pk)
        
        if user.exists():
            raise forms.ValidationError("A user with that email already exists")
        
        return self.cleaned_data.get('email')

    def change_password(self):
        if 'new_password' in self.data and 'confirm_password' in self.data:
            new_password = self.data['new_password']
            confirm_password = self.data['confirm_password']
            if new_password != '' and confirm_password != '':
                if new_password != confirm_password:
                    raise forms.ValidationError("Passwords do not match")
                else:
                    self.instance.set_password(new_password)
                    self.instance.save()

    def clean(self):
        self.change_password()

#Update DP
class ProfilePictureUpdateForm(forms.Form):
    profile_image = forms.ImageField(required=True)

        
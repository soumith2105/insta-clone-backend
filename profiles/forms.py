from django import forms
from .models import UserProfile


class UserCreationForm(forms.ModelForm):

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = UserProfile
        fields = ('username', 'email_id',)

    def clean_username(self):
        username = self.cleaned_data["username"]
        return username.casefold()

    def clean_email_id(self):
        email_id = self.cleaned_data['email_id']
        return email_id.casefold()

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):

    #password = ReadOnlyPasswordHashField()
    def clean_username(self):
        username = self.cleaned_data["username"]
        return username.casefold()

    def clean_email_id(self):
        email_id = self.cleaned_data['email_id']
        return email_id.casefold()

    class Meta:
        model = UserProfile
        fields = ('username', 'email_id', 'full_name', 'date_of_birth', 'mobile_number', 'bio',)

    # def clean_password(self):
    #     return self.initial["password"]

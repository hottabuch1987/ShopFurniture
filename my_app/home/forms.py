from captcha.fields import ReCaptchaField
from django import forms
from .models import *
from account.models import Reviews


class ContactForm(forms.ModelForm):
    captcha = ReCaptchaField()

    class Meta:
        model = Feedback
        fields = ('email_contact', 'firstname_contact', 'text_contact', 'captcha')



class SearchForm(forms.Form):
    q = forms.CharField(label='Search')



class AddPostForm(forms.ModelForm):
    captcha = ReCaptchaField()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].empty_label = "Продукт не выбран"

    class Meta:
        model = Reviews
        fields = [ 'product',  'captcha']


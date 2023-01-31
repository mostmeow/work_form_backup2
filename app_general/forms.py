from django import forms
from django.forms import ModelForm

from .models import *

class RegisterForm(forms.ModelForm):
    channel = forms.ModelMultipleChoiceField(queryset=ChannelModel.objects.all(), widget=forms.CheckboxSelectMultiple, required=True)
    receipt = forms.ChoiceField(choices=RECEIPTTYPE, widget=forms.RadioSelect)
    paymenttype = forms.ChoiceField(choices=PAYMENTTYPE, widget=forms.RadioSelect)
    paywithvoucher = forms.ChoiceField(choices=PAYMENVOUCHERTTYPE, widget=forms.RadioSelect, required=False)
    class Meta:
        model = RegisterModel
        fields = {'channel','receipt','paymenttype','paywithvoucher'}

class UploadImageForm(ModelForm):
    class Meta:
        model = RegisterModel
        fields = ['imageevidence', 'imagevoucherevidence']
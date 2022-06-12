from django import forms
from matplotlib.pyplot import cla, text

class TextForm(forms.Form): #Comment Form
    text = forms.CharField(widget=forms.Textarea , required=True)
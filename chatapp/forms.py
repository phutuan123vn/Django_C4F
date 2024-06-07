from django import forms
from .models import Message as me
from .models import Code as co



class MessageForm(forms.ModelForm):
    class Meta:
        model = me
        fields = ['value']
    value = forms.CharField(label='Message', max_length=1000, widget=forms.Textarea(attrs={'rows': 5, 'cols': 50}))
    
    
    def clean_message(self):
        data:str = self.cleaned_data['value']
        if not data.strip():
            raise forms.ValidationError('You must write something')
        return data
    

class CodeForm(forms.ModelForm):
    class Meta:
        model = co
        fields = ['code']
    
    code = forms.TextInput(attrs={'placeholder': 'Enter code here to join a room'})
    
    def clean(self):
        cleaned_data = super().clean()
        code:str = cleaned_data['code']
        if not code.strip():
            raise forms.ValidationError('You must enter a code')
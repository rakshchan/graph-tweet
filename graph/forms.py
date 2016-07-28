from django import forms

class UserHandle(forms.Form):
	handle = forms.CharField(label='Twitter-User-Handle', max_length=30)
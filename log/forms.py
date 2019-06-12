from .models import Contact, Call
from django import forms

class ContactForm(forms.ModelForm):

	class Meta:
		model = Contact
		exclude = ['person_who_saved',]

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['username'].widget.attrs.update({'class': 'form-control'})
		self.fields['phone'].widget.attrs.update({'class': 'form-control'})
		self.fields['email'].widget.attrs.update({'class': 'form-control'})
		self.fields['address'].widget.attrs.update({'class': 'form-control'})
		self.fields['category'].widget.attrs.update({'class': 'form-control'})


class CallForm(forms.ModelForm):

	class Meta:
		model = Call
		fields = ['call_to', 'msg']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['call_to'].widget.attrs.update({'class': 'form-control'})
		self.fields['msg'].widget.attrs.update({'class': 'form-control',
												'placeholder': 'Write Your message...'})


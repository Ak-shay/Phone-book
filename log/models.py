from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from validators.phone_validator import validate_phone

CATEGORY_CHOICES = [
	('Mobile', 'Mobile'),
	('Work', 'Work'),
	('Home', 'Home'),
	('Fax', 'Fax')
]

class Contact(models.Model):
	person_who_saved = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	username = models.CharField(max_length=30, blank=True)
	phone = models.CharField(max_length=10, validators=[validate_phone])
	email = models.EmailField(blank=True)
	address = models.CharField(max_length=100, blank=True)
	is_fav = models.BooleanField(default=False)
	category = models.CharField(choices=CATEGORY_CHOICES, max_length=15, default='Mobile')

	def __unicode__(self):
		return self.phone

	def get_absolute_url(self):
		return reverse('log:contact_detail', kwargs={'pk': self.pk})

	def name(self):
		try:
			name = self.username
		except:
			name = self.phone
		return name

class Call(models.Model):
	call_from = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	call_to = models.CharField(max_length=10, validators=[validate_phone])
	is_missed = models.BooleanField(default=True)
	made_on = models.DateTimeField()
	duration = models.DurationField(blank=True, null=True)
	msg = models.CharField(max_length=150, blank=True)

	def __unicode__(self):
		return self.call_from

	def get_absolute_url(self):
		return reverse('log:call_detail', kwargs={'pk': self.pk})

	def saved_name(self, user):
		if self.call_from == user: #outgoing
			try:
				return user.contact_set.get(phone=self.call_to).name()
			except:
				return self.call_to

		elif self.call_to == user.phone: #incoming
			try:
				return user.contact_set.get(phone=self.call_from).name()
			except:
				return self.call_from
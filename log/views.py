from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, UpdateView, CreateView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Call, Contact
from .forms import CallForm, ContactForm
from django.utils import timezone
from itertools import chain


class ContactListView(LoginRequiredMixin, ListView):
	context_object_name = 'contacts'
	template_name = 'log/contact_list.html'

	def get_queryset(self):
		queryset = Contact.objects.filter(person_who_saved=self.request.user).order_by('username')
		return queryset

class ContactView(LoginRequiredMixin, View):
	template_name = 'log/contact_detail.html'
	context_object_name = 'contact'

	def get(self, request, pk=None, *args, **kwargs):
		context = {}
		if pk is not None:
			contact = get_object_or_404(Contact, pk=pk)
			context[self.context_object_name] = contact
		return render(request, self.template_name, context)

	def post(self, request, pk, *args, **kwargs):
		contact = get_object_or_404(Contact, pk=pk)

		if request.POST.get('delete') == 'done':
			if contact.person_who_saved == request.user:
				contact.delete()
				return redirect('log:contact_list')

		if request.POST.get('call') == 'done':
 			call = Call.objects.create(call_from=request.user, call_to=contact.phone, made_on=timezone.now())
 			return redirect('log:logs', log='outgoing')			


class ContactCreateView(LoginRequiredMixin, CreateView):
	model = Contact
	template_name = 'log/contact_form.html'
	form_class = ContactForm

	def form_valid(self, form):
		contact = form.save(commit=False)
		contact.person_who_saved = self.request.user
		contact.save()
		return super().form_valid(form)

class ContactUpdateView(LoginRequiredMixin, UpdateView):
	model = Contact
	template_name = 'log/contact_form.html'
	form_class = ContactForm


class CallListView(LoginRequiredMixin, ListView):
	context_object_name = 'logs'
	template_name = 'log/call_list.html'
	model = Call

	def get_queryset(self):
		log = self.kwargs['log']

		phone = self.request.user.phone
		outgoing = Call.objects.filter(call_from=self.request.user).order_by('-made_on')
		incoming = Call.objects.filter(call_to=phone).order_by('-made_on')
		logs = sorted(chain(incoming, outgoing),
					  key=lambda Call: Call.made_on,
					  reverse=True)

		if log == 'incoming':
			queryset = incoming

		elif log == 'outgoing':
			queryset = outgoing

		elif log == 'all':
			queryset = logs

		return queryset

class CallFormView(LoginRequiredMixin, CreateView):
	model = Call
	template_name = 'log/call_form.html'
	form_class = CallForm

	def form_valid(self, form):
		if self.request.POST.get('call') == 'done':
			call = form.save(commit=False)
			call.call_from = self.request.user
			call.made_on = timezone.now()
			call.save()
			return super().form_valid(form)

		if self.request.POST.get('save') == 'done':
			contact = Contact.objects.create(person_who_saved=self.request.user, phone=form.instance.call_to)
			print(contact)
			return redirect('log:edit_contact', pk=contact.pk)

class CallView(LoginRequiredMixin, View):
	template_name= 'log/call_detail.html'
	context_object_name = 'call'

	def get(self, *args, **kwargs):
		pk = self.kwargs['pk']
		context = {}
		if pk is not None:
			contact = get_object_or_404(Call, pk=pk)
			context[self.context_object_name] = contact
		return render(self.request, self.template_name, context)

	def post(self, *args, **kwargs):
		pk = self.kwargs['pk']
		print(pk)
		call = get_object_or_404(Call, pk=pk)

		if self.request.POST.get('delete') == 'done':
			print(call)
			if call.call_from == self.request.user or call.call_to == self.request.user.phone:
				call.delete()
				return redirect('log:logs', log='all')
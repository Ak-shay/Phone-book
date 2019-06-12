from django.urls import path
from . import views

app_name = 'log'

urlpatterns = [
	path('contact/', views.ContactListView.as_view(), name='contact_list'),
	path('contact/<int:pk>/', views.ContactView.as_view(), name='contact_detail'),
	path('logs/<str:log>/', views.CallListView.as_view(), name='logs'),
	path('contact/edit/<int:pk>/', views.ContactUpdateView.as_view(), name='edit_contact'),
	path('create/', views.ContactCreateView.as_view(), name='contact_create'),
	path('call/', views.CallFormView.as_view(), name='make_call'),
	path('call/<int:pk>/detail/', views.CallView.as_view(), name='call_detail'),

]
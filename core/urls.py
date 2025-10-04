from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    # Basic pages
    path('', views.home_view, name='home_view'),
    path('about/', views.about_view, name='about_view'),
    path('service/', views.service_view, name='service_view'),
    path('contact/', views.contact_view, name='contact_view'),
    
    # Authentication
    path('login/', LoginView.as_view(template_name='core/login.html'), name='login_view'),
    path('logout/', LogoutView.as_view(), name='logout_view'),
    path('signup/', views.signup_view, name='signup_view'),
    
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard_view'),
    
    # Client management
    path('client/add/', views.add_client, name='add_client_view'),
    path('client/<int:client_id>/view/', views.client_view, name='client_view'),
    path('client/<int:client_id>/edit-medical/', views.edit_client_medical, name='edit_client_medical'),
    
    # Referrals
    path('refer-client/', views.refer_client, name='refer_client'),
    path('complete-referral/<int:client_id>/', views.complete_referral, name='complete_referral'),
    path('client/<int:client_id>/complete-referral/', views.complete_referral, name='complete_referral'),
    path('pending-referrals/', views.pending_referrals_view, name='pending_referrals_view'),
    path('mark-referral-seen/<int:client_id>/', views.mark_referral_seen, name='mark_referral_seen'),
    
    # Notifications
    path('check-notifications/', views.check_notifications, name='check_notifications'),
    path('client/<int:client_id>/delete/', views.delete_client, name='delete_client'),
]
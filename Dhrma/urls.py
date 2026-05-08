from django.urls import path

from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('manufacturing/', views.manufacturing, name='manufacturing'),
    path('products/', views.products, name='products'),
    path('gallery/', views.gallery, name='gallery'),
    path('contact/', views.contact, name='contact'),
    path('sample/<slug:fabric>/', views.sample_request, name='sample_request'),
    path('product/<int:id>/inquiry/', views.inquiry, name='inquiry'),
    path('newsletter/', views.newsletter_signup, name='newsletter_signup'),
    path('factory-visit/', views.factory_visit, name='factory_visit'),
    path('legal/<slug:page>/', views.legal_page, name='legal_page'),
    path('privacy/', views.legal_page, {'page': 'privacy'}, name='privacy'),
    path('terms/', views.legal_page, {'page': 'terms'}, name='terms'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('bulk/', views.bulk_order_form, name='bulk_order_form'),
    path('bulk/success/<int:order_id>/', views.bulk_order_success, name='bulk_order_success'),
    path('employee/', views.employee_dashboard, name='employee_dashboard'),
]
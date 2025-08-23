from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from orders.views import RoleBasedLoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('orders/', include('orders.urls')),
    path('login/', RoleBasedLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

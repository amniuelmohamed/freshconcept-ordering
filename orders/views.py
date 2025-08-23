from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Customer, Order, Product, OrderItem
from datetime import datetime
from django.contrib.auth.views import LoginView
from django.urls import reverse

class RoleBasedLoginView(LoginView):
    template_name = 'registration/login.html'

    def get_success_url(self):
        user = self.request.user
        if hasattr(user, 'role'):
            if user.role == 'customer':
                return reverse('bulk_order_form')
            elif user.role == 'employee':
                return reverse('employee_dashboard')
            elif user.role == 'admin':
                return reverse('admin:index')
        return super().get_success_url()

@login_required
def bulk_order_form(request):
    try:
        customer = request.user.customer_profile
    except Customer.DoesNotExist:
        return HttpResponse('Unauthorized', status=401)

    all_active_products = Product.objects.filter(is_active=True)
    last_orders = list(Order.objects.filter(customer=customer).order_by('-order_date').values('id', 'order_date')[:3])
    order_ids = [o['id'] for o in last_orders]
    order_dates = [o['order_date'] for o in last_orders]
    for product in all_active_products:
        product.last_order_quantities = product.quantities_for_orders(order_ids)
        # Calculate margin percentage for display
        product.margin_percentage = int(float(product.margin_rate) * 100)

    _, next_delivery_day_name, next_delivery_date = customer.get_next_delivery_day_info()

    errors = {}
    quantities = {}

    if request.method == 'POST':
        # Collect quantities and validate
        for product in all_active_products:
            key = f'quantity_{product.id}'
            value = request.POST.get(key)
            quantities[product.id] = value  # Save entered value for re-rendering
            try:
                quantity = int(value) if value else 0
                if quantity > 0 and quantity < product.minimum_quantity:
                    errors[product.id] = f"Minimum: {product.minimum_quantity}"
            except (TypeError, ValueError):
                errors[product.id] = "Enter a valid number"

        if errors:
            context = {
                'customer': customer,
                'all_active_products': all_active_products,
                'order_dates': order_dates,
                'errors': errors,
                'quantities': quantities,
                'next_delivery_day_name': next_delivery_day_name,
                'next_delivery_date': next_delivery_date,
            }
            return render(request, 'orders/bulk_order_form.html', context)
        
        # Clear errors if no validation issues
        errors = {}
        quantities = {}

        # No errors: create order and order items
        order = Order.objects.create(
            customer=customer,
            order_date=datetime.now(),
            delivery_date=next_delivery_date.date() if next_delivery_date else None,
        )
        for product in all_active_products:
            key = f'quantity_{product.id}'
            value = request.POST.get(key)
            try:
                quantity = int(value) if value else 0
            except (TypeError, ValueError):
                continue  # Should not happen if validated above
            if quantity > 0:
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                )
        
        # Redirect to success page to prevent form re-rendering with old data
        return redirect('bulk_order_success', order_id=order.id)

    # GET request
    context = {
        'customer': customer,
        'all_active_products': all_active_products,
        'order_dates': order_dates,
        'errors': {},  # Always start with empty errors on GET
        'quantities': {},  # Always start with empty quantities on GET
        'next_delivery_day_name': next_delivery_day_name,
        'next_delivery_date': next_delivery_date,
    }
    return render(request, 'orders/bulk_order_form.html', context)

@login_required
def bulk_order_success(request, order_id):
    order = Order.objects.get(id=order_id)
    if not order or order.customer != request.user.customer_profile:
        return redirect('bulk_order_form')
    return render(request, 'orders/bulk_order_success.html', {'order': order})


@login_required
def employee_dashboard(request):
    if not request.user.is_employee:
        return HttpResponse('Unauthorized', status=401)
    return render(request, 'orders/employee_dashboard.html')
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

    def dispatch(self, request, *args, **kwargs):
        # If user is already authenticated, redirect them to appropriate page
        if request.user.is_authenticated:
            return redirect(self.get_success_url())
        return super().dispatch(request, *args, **kwargs)

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

    # Check if there's an existing order for the next delivery date
    existing_order = None
    if next_delivery_date:
        existing_order = customer.get_existing_order_for_delivery_date(next_delivery_date.date())

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

        # Check if we're updating an existing order or creating a new one
        if existing_order:
            # Update existing order
            order = existing_order
            # Clear existing order items
            order.order_items.all().delete()
            order.save()
        else:
            # Create new order
            if not next_delivery_date:
                # If no delivery date available, redirect back with error
                context = {
                    'customer': customer,
                    'all_active_products': all_active_products,
                    'order_dates': order_dates,
                    'errors': {'general': 'No delivery date available. Please contact support.'},
                    'quantities': quantities,
                    'next_delivery_day_name': next_delivery_day_name,
                    'next_delivery_date': next_delivery_date,
                }
                return render(request, 'orders/bulk_order_form.html', context)
            
            order = Order.objects.create(
                customer=customer,
                order_date=datetime.now(),
                delivery_date=next_delivery_date.date(),
            )

        # Create or update order items
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

    # GET request - pre-fill form with existing order data if available
    if existing_order:
        # Pre-fill quantities from existing order
        for product in all_active_products:
            try:
                order_item = existing_order.order_items.get(product=product)
                quantities[product.id] = order_item.quantity
            except OrderItem.DoesNotExist:
                quantities[product.id] = 0
    else:
        quantities = {}  # Empty quantities for new order

    context = {
        'customer': customer,
        'all_active_products': all_active_products,
        'order_dates': order_dates,
        'errors': {},  # Always start with empty errors on GET
        'quantities': quantities,  # Pre-filled or empty quantities
        'next_delivery_day_name': next_delivery_day_name,
        'next_delivery_date': next_delivery_date,
        'existing_order': existing_order,  # Pass to template for UI feedback
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
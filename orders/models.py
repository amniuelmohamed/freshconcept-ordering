"""
GMS Ordering System for FreshConcept Charcuterie

Django models for managing orders from FreshConcept charcuterie supplier.
Specifically designed for GMS (Grandes et Moyennes Surfaces) customers - 
supermarkets and retail chains.

Models:
    - Customer: GMS locations/stores (supermarkets, retail chains)
    - Product: Charcuterie products from FreshConcept
    - Order: Purchase orders to FreshConcept
    - OrderItem: Individual products in each order
"""

from django.db import models
from django.core.validators import RegexValidator
from decimal import Decimal
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """
    Custom user model extending Django's AbstractUser with role-based access control.
    
    Roles:
        - customer: Can place orders and view order history
        - employee: Can manage products, customers, and orders
        - admin: Full system access including user management
    
    Each customer has a one-to-one relationship with a User account.
    """
    ROLE_CHOICES = [
        ('customer', 'Customer'),
        ('employee', 'Employee'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')

    def __str__(self):
        return f'{self.username} - {self.get_role_display()}'

    @property
    def is_customer(self):
        return self.role == 'customer'
    
    @property
    def is_employee(self):
        return self.role in ['employee', 'admin']
    
    @property
    def is_admin(self):
        return self.role == 'admin'


class Customer(models.Model):
    """
    GMS locations/stores (supermarkets, retail chains) that place orders with FreshConcept.
    
    Each customer is linked to a User account and has a delivery schedule that determines
    when they can place orders and when deliveries occur.
    
    Delivery Schedule Format:
        {"1": ["0", "08:00"], "4": ["3", "08:00"]}
        - Key: delivery_day (0=Monday, 1=Tuesday, etc.)
        - Value: [order_day, deadline_time]
        - Example: {"1": ["0", "08:00"]} means Tuesday delivery, order by Monday 8 AM
    """
    
    # Belgian VAT number validator (10 digits starting with 0 or 1)
    vat_validator = RegexValidator(
        r"^[01]\d{9}$", 
        "Belgian VAT number must be 10 digits starting with 0 or 1"
    )

    # Belgian phone number validator (including GSM)
    phone_validator = RegexValidator(
        r"^(\+32|0)[1-9]\d{7,8}$", 
        "Phone number must be a valid Belgian number"
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile')
    customer_number = models.CharField(max_length=20, unique=True)
    company_name = models.CharField(max_length=255)
    address = models.TextField()
    vat_number = models.CharField(
        max_length=10, 
        unique=True, 
        blank=True, 
        null=True, 
        validators=[vat_validator]
    )
    contact_person = models.CharField(max_length=255)
    phone_number = models.CharField(
        max_length=15, 
        unique=True, 
        validators=[phone_validator]
    )
    
    delivery_schedule = models.JSONField(
        default=dict,
        help_text="Delivery schedule: {'1': ('0', '08:00'), '4': ('3', '08:00')} where key=delivery_day, value=(order_day, deadline_time)"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.customer_number} - {self.company_name.title()}"

    def get_delivery_days_display(self):
        """Get human-readable delivery days."""
        day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        return [day_names[int(day)] for day in self.delivery_schedule.keys()]
    
    def get_next_delivery_day(self):
        """Get the next available delivery day."""
        from datetime import datetime
        
        today = datetime.now().weekday()
        
        # Get all delivery days from the schedule
        delivery_days = [int(day) for day in self.delivery_schedule.keys()]
        
        if not delivery_days:
            return None
        
        # Sort delivery days
        delivery_days.sort()
        
        # Find next delivery day this week
        for day in delivery_days:
            if day > today:
                return day
        
        # If no days this week, return first day of next week
        return delivery_days[0] if delivery_days else None

    def can_order_for_delivery(self, delivery_day):
        """Check if customer can still order for a specific delivery day."""
        from datetime import datetime
        
        if str(delivery_day) not in self.delivery_schedule:
            return False
        
        order_day, deadline_time = self.delivery_schedule[str(delivery_day)]
        today = datetime.now().weekday()
        
        # If today is the order day, check if deadline has passed
        if today == int(order_day):
            current_time = datetime.now().time()
            deadline = datetime.strptime(deadline_time, '%H:%M').time()
            return current_time < deadline
        
        # If today is after the order day, it's too late
        elif today > int(order_day):
            return False
        
        # If today is before the order day, still have time
        else:
            return True


class Product(models.Model):
    """
    Charcuterie products available from FreshConcept.
    """
    
    name = models.CharField(max_length=255)
    description = models.TextField()
    price_per_kg = models.DecimalField(
        max_digits=8, 
        decimal_places=2,
        help_text="Wholesale price per kilogram"
    )
    margin_rate = models.DecimalField(
        max_digits=5, 
        decimal_places=4, 
        default=0.30
    )
    retail_price_override = models.DecimalField(
        max_digits=8, 
        decimal_places=2, 
        blank=True, 
        null=True
    )
    approximate_weight = models.DecimalField(max_digits=8, decimal_places=3)
    minimum_quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def wholesale_price(self):
        """Calculate wholesale price based on price per kg and weight."""
        if not self.price_per_kg or not self.approximate_weight:
            return Decimal('0.00')
        return round(self.price_per_kg * self.approximate_weight, 2)

    @property
    def retail_price(self):
        """Calculate retail price with margin or return manual override."""
        if self.retail_price_override:
            return self.retail_price_override
        # Calculate: (price_per_kg × weight + 6% VAT) × (1 + margin)
        if not self.price_per_kg or not self.approximate_weight:
            return Decimal('0.00')
        wholesale_total = self.price_per_kg * self.approximate_weight
        return round(wholesale_total * Decimal("1.06") * (Decimal("1") + self.margin_rate), 2)

    @property
    def price_per_kg_retail(self):
        """Calculate retail price per kilogram."""
        if self.retail_price_override and self.approximate_weight:
            return round(self.retail_price_override / self.approximate_weight, 2)
        # Calculate: price_per_kg × 1.06 × (1 + margin)
        if not self.price_per_kg:
            return Decimal('0.00')
        return round(self.price_per_kg * Decimal("1.06") * (Decimal("1") + self.margin_rate), 2)

    def __str__(self):
        weight = f"{self.approximate_weight}kg" if self.approximate_weight else "No weight set"
        return f"{self.name} - {weight}"


class Order(models.Model):
    """
    Purchase orders from GMS customers to FreshConcept charcuterie supplier.
    """
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def total_amount(self):
        """Calculate total amount from order items."""
        if not self.pk:
            return Decimal('0.00')
        return sum(item.total_price for item in self.order_items.all())
    
    def __str__(self):
        return f"Order {self.id} - {self.customer.company_name}"
    
    @property
    def total_items(self):
        """Calculate total number of items in the order."""
        if not self.pk:
            return 0
        return sum(item.quantity for item in self.order_items.all())


class OrderItem(models.Model):
    """
    Individual charcuterie products in each order.
    """
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    class Meta:
        unique_together = ['order', 'product']
    
    def save(self, *args, **kwargs):
        """Auto-calculate unit_price and total_price if not set."""
        try:
            if not self.unit_price and hasattr(self.product, 'wholesale_price'):
                self.unit_price = self.product.wholesale_price
            if not self.total_price and self.unit_price:
                self.total_price = self.quantity * self.unit_price
        except (AttributeError, TypeError):
            # If we can't calculate prices, set defaults
            if not self.unit_price:
                self.unit_price = Decimal('0.00')
            if not self.total_price:
                self.total_price = Decimal('0.00')
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.quantity}x {self.product.name} - €{self.total_price}"
        
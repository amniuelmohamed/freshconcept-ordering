from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Customer, Product, Order, OrderItem

admin.site.register(User, UserAdmin)

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    """
    Admin interface for Customer model.
    
    Features:
        - User account linking (one-to-one with User model)
        - Delivery schedule management via JSON field
        - Business information management
        - Automatic timestamp tracking
    """
    list_display = ['customer_number', 'company_name', 'contact_person', 'user', 'phone_number', 'delivery_schedule_display']
    list_filter = ['created_at']
    search_fields = ['customer_number', 'company_name', 'contact_person', 'user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['company_name']
    
    fieldsets = (
        ('User Account', {
            'fields': ('user',)
        }),
        ('Basic Information', {
            'fields': ('customer_number', 'company_name', 'address', 'contact_person', 'phone_number')
        }),
        ('Business Details', {
            'fields': ('vat_number',)
        }),
        ('Delivery Schedule', {
            'fields': ('delivery_schedule',),
            'description': 'Format: {"1": ["0", "08:00"], "4": ["3", "08:00"]} where key=delivery_day, value=[order_day, deadline_time]'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def delivery_schedule_display(self, obj):
        """Display delivery schedule in human-readable format."""
        try:
            days = obj.get_delivery_days_display()
            return ', '.join(days) if days else 'No delivery days set'
        except (AttributeError, IndexError, TypeError):
            return 'No delivery days set'
    delivery_schedule_display.short_description = 'Delivery Days'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_price_per_kg_display', 'get_wholesale_price', 'get_retail_price', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['get_wholesale_price', 'get_retail_price', 'get_price_per_kg_retail_display', 'created_at', 'updated_at']
    ordering = ['name']

    def get_price_per_kg_display(self, obj):
        """Display the price per kg with currency symbol."""
        try:
            if obj.price_per_kg:
                return f"€{obj.price_per_kg}"
            return "€0.00"
        except (AttributeError, TypeError):
            return "€0.00"
    get_price_per_kg_display.short_description = 'Price per KG'

    def get_price_per_kg_retail_display(self, obj):
        """Display the retail price per kg with currency symbol."""
        try:
            if obj.price_per_kg_retail:
                return f"€{obj.price_per_kg_retail}"
            return "€0.00"
        except (AttributeError, TypeError):
            return "€0.00"
    get_price_per_kg_retail_display.short_description = 'Retail Price per KG'
    
    
    def get_wholesale_price(self, obj):
        """Display the calculated wholesale price."""
        try:
            if obj.wholesale_price:
                return f"€{obj.wholesale_price}"
            return "€0.00"
        except (AttributeError, TypeError):
            return "€0.00"
    get_wholesale_price.short_description = 'Wholesale Price'
    
    def get_retail_price(self, obj):
        """Display the calculated retail price."""
        try:
            if obj.retail_price:
                return f"€{obj.retail_price}"
            return "€0.00"
        except (AttributeError, TypeError):
            return "€0.00"
    get_retail_price.short_description = 'Retail Price'


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    readonly_fields = ['unit_price', 'total_price']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'order_date', 'delivery_date', 'status', 'get_total_amount', 'get_total_items']
    list_filter = ['status', 'order_date', 'delivery_date', 'created_at']
    search_fields = ['customer__company_name', 'customer__customer_number']
    readonly_fields = ['order_date', 'delivery_date', 'created_at', 'updated_at']
    inlines = [OrderItemInline]
    ordering = ['-order_date']
    
    def get_total_amount(self, obj):
        """Display the calculated total amount."""
        try:
            return f"€{obj.total_amount}"
        except (AttributeError, TypeError):
            return "€0.00"
    get_total_amount.short_description = 'Total Amount'
    
    def get_total_items(self, obj):
        """Display the calculated total items."""
        try:
            return obj.total_items
        except (AttributeError, TypeError):
            return 0
    get_total_items.short_description = 'Total Items'


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'unit_price', 'total_price']
    list_filter = ['order__status', 'order__order_date']
    search_fields = ['order__customer__company_name', 'product__name']
    readonly_fields = ['unit_price', 'total_price']

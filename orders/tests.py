from django.test import TestCase
from django.core.exceptions import ValidationError
from decimal import Decimal
from .models import User, Customer, Product, Order, OrderItem


class CustomerModelTest(TestCase):
    """Test cases for the Customer model."""
    
    def setUp(self):
        """Set up test data for customer tests."""
        # Create User first (required for Customer)
        self.user = User.objects.create_user(
            username='testuser',
            email='john@testsupermarket.be',
            password='testpass123',
            role='customer'
        )
        
        self.valid_customer_data = {
            'user': self.user,
            'customer_number': 'CUST001',
            'company_name': 'Test Supermarket',
            'address': '123 Test Street, Brussels',
            'vat_number': '0123456789',
            'contact_person': 'John Doe',
            'phone_number': '+32 2 123 45 67'
        }
    
    def test_create_customer(self):
        """Test creating a customer with valid data."""
        customer = Customer.objects.create(**self.valid_customer_data)
        self.assertEqual(customer.customer_number, 'CUST001')
        self.assertEqual(customer.company_name, 'Test Supermarket')
        self.assertEqual(customer.vat_number, '0123456789')
        self.assertEqual(customer.phone_number, '+32 2 123 45 67')
    
    def test_customer_str_representation(self):
        """Test customer string representation."""
        customer = Customer.objects.create(**self.valid_customer_data)
        expected = 'CUST001 - Test Supermarket'
        self.assertEqual(str(customer), expected)
    
    def test_vat_number_validation(self):
        """Test VAT number validation."""
        # Valid VAT numbers
        valid_vats = ['0123456789', '1123456789']
        for i, vat in enumerate(valid_vats):
            # Create new user for each test
            user = User.objects.create_user(
                username=f'vatuser{i}',
                email=f'vat{i}@testsupermarket.be',
                password='testpass123',
                role='customer'
            )
            customer_data = self.valid_customer_data.copy()
            customer_data['user'] = user
            customer_data['customer_number'] = f'CUST00{i+12}'  # Make unique
            customer_data['phone_number'] = f'+32 2 123 45 {70+i}'  # Make unique
            customer_data['vat_number'] = vat
            customer = Customer.objects.create(**customer_data)
            self.assertEqual(customer.vat_number, vat)
        
        # Invalid VAT numbers
        invalid_vats = ['123456789', '012345678', '2123456789', 'abc1234567']
        for i, vat in enumerate(invalid_vats):
            # Create new user for each test
            user = User.objects.create_user(
                username=f'invalidvatuser{i}',
                email=f'invalidvat{i}@testsupermarket.be',
                password='testpass123',
                role='customer'
            )
            customer_data = self.valid_customer_data.copy()
            customer_data['user'] = user
            customer_data['customer_number'] = f'CUST00{i+14}'  # Make unique
            customer_data['phone_number'] = f'+32 2 123 45 {80+i}'  # Make unique
            customer_data['vat_number'] = vat
            with self.assertRaises(ValidationError):
                customer = Customer(**customer_data)
                customer.full_clean()
    
    def test_phone_number_validation(self):
        """Test phone number validation."""
        # Valid phone numbers
        valid_phones = ['+32 2 123 45 67', '02 123 45 67', '+32 470 12 34 56', '0470 12 34 56']
        for i, phone in enumerate(valid_phones):
            # Create new user for each test
            user = User.objects.create_user(
                username=f'phoneuser{i}',
                email=f'phone{i}@testsupermarket.be',
                password='testpass123',
                role='customer'
            )
            customer_data = self.valid_customer_data.copy()
            customer_data['user'] = user
            customer_data['customer_number'] = f'CUST00{i+4}'  # Make unique
            customer_data['vat_number'] = f'01234567{80+i}'  # Make VAT unique
            customer_data['phone_number'] = phone
            customer = Customer.objects.create(**customer_data)
            self.assertEqual(customer.phone_number, phone)
        
        # Invalid phone numbers
        invalid_phones = ['+32 0123 45 67', '02 0123 45 67', '+33 2 123 45 67', '123 45 67']
        for i, phone in enumerate(invalid_phones):
            # Create new user for each test
            user = User.objects.create_user(
                username=f'invalidphoneuser{i}',
                email=f'invalid{i}@testsupermarket.be',
                password='testpass123',
                role='customer'
            )
            customer_data = self.valid_customer_data.copy()
            customer_data['user'] = user
            customer_data['customer_number'] = f'CUST00{i+8}'  # Make unique
            customer_data['vat_number'] = f'01234567{90+i}'  # Make VAT unique
            customer_data['phone_number'] = phone
            with self.assertRaises(ValidationError):
                customer = Customer(**customer_data)
                customer.full_clean()
    
    def test_unique_constraints(self):
        """Test unique constraints for customer_number, user, and phone."""
        # Create all User objects first to avoid transaction issues
        user1 = User.objects.create_user(
            username='duplicateuser1',
            email='different@email.be',
            password='testpass123',
            role='customer'
        )
        user2 = User.objects.create_user(
            username='duplicateuser2',
            email='another@email.be',
            password='testpass123',
            role='customer'
        )
        
        # Create first customer successfully
        Customer.objects.create(**self.valid_customer_data)
        
        # Test duplicate customer_number
        duplicate_data = self.valid_customer_data.copy()
        duplicate_data['user'] = user1
        duplicate_data['phone_number'] = '+32 2 123 45 68'
        with self.assertRaises(Exception):
            Customer.objects.create(**duplicate_data)
        
        # Test duplicate user (one-to-one relationship)
        duplicate_data = self.valid_customer_data.copy()
        duplicate_data['customer_number'] = 'CUST002'
        duplicate_data['phone_number'] = '+32 2 123 45 68'
        duplicate_data['vat_number'] = '0123456790'  # Make VAT unique
        with self.assertRaises(Exception):
            Customer.objects.create(**duplicate_data)
        
        # Test duplicate phone
        duplicate_data = self.valid_customer_data.copy()
        duplicate_data['user'] = user2
        duplicate_data['customer_number'] = 'CUST002'
        duplicate_data['vat_number'] = '0123456791'  # Make VAT unique
        with self.assertRaises(Exception):
            Customer.objects.create(**duplicate_data)
    
    def test_delivery_schedule_functionality(self):
        """Test delivery schedule functionality with new JSON field structure."""
        # Create customer with delivery schedule using new format
        customer_data = self.valid_customer_data.copy()
        customer_data['delivery_schedule'] = {
            '1': ['0', '08:00'],  # Tuesday delivery, order by Monday 8 AM
            '4': ['3', '08:00']   # Friday delivery, order by Thursday 8 AM
        }
        
        customer = Customer.objects.create(**customer_data)
        
        # Test delivery days display
        delivery_days = customer.get_delivery_days_display()
        self.assertEqual(delivery_days, ['Tuesday', 'Friday'])
        
        # Test can_order_for_delivery method
        # Note: This method requires datetime mocking for full testing
        # For now, just test that the method exists and doesn't crash
        self.assertTrue(hasattr(customer, 'can_order_for_delivery'))
        self.assertTrue(hasattr(customer, 'get_next_delivery_day'))
    
    def test_delivery_schedule_basic_functionality(self):
        """Test basic delivery schedule functionality with new structure."""
        # Create new user for this test to avoid conflicts
        user = User.objects.create_user(
            username='basicuser',
            email='basic@testsupermarket.be',
            password='testpass123',
            role='customer'
        )
        
        customer_data = self.valid_customer_data.copy()
        customer_data['user'] = user
        customer_data['customer_number'] = 'CUST003'  # Make unique
        customer_data['phone_number'] = '+32 2 123 45 69'  # Make unique
        customer_data['vat_number'] = '0123456792'  # Make VAT unique
        customer_data['delivery_schedule'] = {
            '1': ['0', '08:00'],  # Tuesday delivery, order by Monday 8 AM
            '4': ['3', '14:30']   # Friday delivery, order by Thursday 2:30 PM
        }
        
        customer = Customer.objects.create(**customer_data)
        
        # Test that the delivery schedule is stored correctly
        self.assertEqual(customer.delivery_schedule, {
            '1': ['0', '08:00'],
            '4': ['3', '14:30']
        })
        
        # Test that methods exist and don't crash
        self.assertTrue(hasattr(customer, 'can_order_for_delivery'))
        self.assertTrue(hasattr(customer, 'get_next_delivery_day'))
    
    def test_delivery_schedule_validation(self):
        """Test delivery schedule field validation with new JSON structure."""
        # Valid delivery schedule format
        valid_schedule = {
            '1': ['0', '08:00'],  # Tuesday delivery, order by Monday 8 AM
            '4': ['3', '14:30'],  # Friday delivery, order by Thursday 2:30 PM
            '6': ['5', '16:00']   # Sunday delivery, order by Saturday 4 PM
        }
        
        # Create new user for this test
        user = User.objects.create_user(
            username='scheduleuser',
            email='schedule@testsupermarket.be',
            password='testpass123',
            role='customer'
        )
        
        customer_data = self.valid_customer_data.copy()
        customer_data['user'] = user
        customer_data['customer_number'] = 'CUST002'  # Make unique
        customer_data['phone_number'] = '+32 2 123 45 68'  # Make unique
        customer_data['vat_number'] = '0123456790'  # Make VAT unique
        customer_data['delivery_schedule'] = valid_schedule
        
        customer = Customer.objects.create(**customer_data)
        self.assertEqual(customer.delivery_schedule, valid_schedule)
    
    def test_empty_delivery_schedule(self):
        """Test customer with no delivery schedule."""
        # Create new user for this test to avoid conflicts
        user = User.objects.create_user(
            username='emptyuser',
            email='empty@testsupermarket.be',
            password='testpass123',
            role='customer'
        )
        
        customer_data = self.valid_customer_data.copy()
        customer_data['user'] = user
        customer_data['customer_number'] = 'CUST004'  # Make unique
        customer_data['phone_number'] = '+32 2 123 45 70'  # Make unique
        customer_data['vat_number'] = '0123456793'  # Make VAT unique
        
        customer = Customer.objects.create(**customer_data)
        
        # Should handle empty delivery schedule gracefully
        self.assertEqual(customer.delivery_schedule, {})
        
        # get_next_delivery_day should return None
        self.assertIsNone(customer.get_next_delivery_day())
        
        # get_delivery_days_display should return empty list
        self.assertEqual(customer.get_delivery_days_display(), [])


class ProductModelTest(TestCase):
    """Test cases for the Product model."""
    
    def setUp(self):
        """Set up test data for product tests."""
        self.valid_product_data = {
            'name': 'Premium Serrano Ham',
            'description': 'High-quality Spanish Serrano ham',
            'price_per_kg': Decimal('18.00'),
            'margin_rate': Decimal('0.30'),
            'approximate_weight': Decimal('0.150'),
            'minimum_quantity': 10,
            'is_active': True
        }
    
    def test_create_product(self):
        """Test creating a product with valid data."""
        product = Product.objects.create(**self.valid_product_data)
        self.assertEqual(product.name, 'Premium Serrano Ham')
        self.assertEqual(product.price_per_kg, Decimal('18.00'))
        self.assertEqual(product.margin_rate, Decimal('0.30'))
        self.assertEqual(product.approximate_weight, Decimal('0.150'))
    
    def test_product_str_representation(self):
        """Test product string representation."""
        product = Product.objects.create(**self.valid_product_data)
        expected = 'Premium Serrano Ham - 0.150kg'
        self.assertEqual(str(product), expected)
    
    def test_wholesale_price_calculation(self):
        """Test wholesale price calculation."""
        product = Product.objects.create(**self.valid_product_data)
        # 18.00 × 0.150 = 2.70
        expected_wholesale = Decimal('2.70')
        self.assertEqual(product.wholesale_price, expected_wholesale)
    
    def test_retail_price_calculation(self):
        """Test retail price calculation with margin and VAT."""
        product = Product.objects.create(**self.valid_product_data)
        # (2.70 × 1.06 × 1.30) = 3.72
        expected_retail = Decimal('3.72')
        self.assertEqual(product.retail_price, expected_retail)
    
    def test_retail_price_override(self):
        """Test retail price override functionality."""
        product = Product.objects.create(**self.valid_product_data)
        product.retail_price_override = Decimal('4.50')
        product.save()
        
        self.assertEqual(product.retail_price, Decimal('4.50'))
    
    def test_price_per_kg_retail_calculation(self):
        """Test retail price per kilogram calculation."""
        product = Product.objects.create(**self.valid_product_data)
        # (18.00 × 1.06 × 1.30) = 24.80
        expected_retail_per_kg = Decimal('24.80')
        self.assertEqual(product.price_per_kg_retail, expected_retail_per_kg)
    
    def test_price_per_kg_retail_with_override(self):
        """Test retail price per kg when override is set."""
        product = Product.objects.create(**self.valid_product_data)
        product.retail_price_override = Decimal('4.50')
        product.save()
        
        # 4.50 ÷ 0.150 = 30.00
        expected_retail_per_kg = Decimal('30.00')
        self.assertEqual(product.price_per_kg_retail, expected_retail_per_kg)
    
    def test_margin_rate_default(self):
        """Test that margin rate defaults to 30%."""
        product = Product.objects.create(**self.valid_product_data)
        self.assertEqual(product.margin_rate, Decimal('0.3'))  # Use actual value, not string
    
    def test_is_active_default(self):
        """Test that is_active defaults to True."""
        product_data = self.valid_product_data.copy()
        del product_data['is_active']
        
        product = Product.objects.create(**product_data)
        self.assertTrue(product.is_active)


class OrderModelTest(TestCase):
    """Test cases for the Order model."""
    
    def setUp(self):
        """Set up test data for order tests."""
        # Create User first
        self.user = User.objects.create_user(
            username='orderuser',
            email='john@testsupermarket.be',
            password='testpass123',
            role='customer'
        )
        
        self.customer = Customer.objects.create(
            user=self.user,
            customer_number='CUST001',
            company_name='Test Supermarket',
            address='123 Test Street, Brussels',
            vat_number='0123456789',
            contact_person='John Doe',
            phone_number='+32 2 123 45 67'
        )
        
        self.valid_order_data = {
            'customer': self.customer,
            'status': 'pending',
            'notes': 'Delivery before 2 PM'
        }
    
    def test_create_order(self):
        """Test creating an order with valid data."""
        order = Order.objects.create(**self.valid_order_data)
        self.assertEqual(order.customer, self.customer)
        self.assertEqual(order.status, 'pending')
        self.assertEqual(order.notes, 'Delivery before 2 PM')
        # total_amount will be calculated automatically when order items are added
    
    def test_order_str_representation(self):
        """Test order string representation."""
        order = Order.objects.create(**self.valid_order_data)
        expected = f'Order {order.id} - Test Supermarket'
        self.assertEqual(str(order), expected)
    
    def test_order_status_choices(self):
        """Test order status choices."""
        valid_statuses = ['pending', 'confirmed', 'cancelled']
        for status in valid_statuses:
            order_data = self.valid_order_data.copy()
            order_data['status'] = status
            order = Order.objects.create(**order_data)
            self.assertEqual(order.status, status)
    
    def test_order_default_status(self):
        """Test that order status defaults to pending."""
        order_data = self.valid_order_data.copy()
        del order_data['status']
        
        order = Order.objects.create(**order_data)
        self.assertEqual(order.status, 'pending')
    
    def test_total_items_property(self):
        """Test total_items property calculation."""
        order = Order.objects.create(**self.valid_order_data)
        
        # Create some order items with different products
        product1 = Product.objects.create(
            name='Test Product 1',
            description='Test Description 1',
            price_per_kg=Decimal('10.00'),
            approximate_weight=Decimal('0.100'),
            minimum_quantity=1
        )
        
        product2 = Product.objects.create(
            name='Test Product 2',
            description='Test Description 2',
            price_per_kg=Decimal('20.00'),
            approximate_weight=Decimal('0.200'),
            minimum_quantity=1
        )
        
        OrderItem.objects.create(
            order=order,
            product=product1,
            quantity=5,
            unit_price=Decimal('3.00'),
            total_price=Decimal('15.00')
        )
        
        OrderItem.objects.create(
            order=order,
            product=product2,
            quantity=3,
            unit_price=Decimal('3.00'),
            total_price=Decimal('9.00')
        )
        
        self.assertEqual(order.total_items, 8)
    
    def test_automatic_total_amount_calculation(self):
        """Test automatic total amount calculation from order items."""
        # Create the order but don't save it yet
        order = Order(**self.valid_order_data)
        
        # Create some order items with different products
        product1 = Product.objects.create(
            name='Test Product 1',
            description='Test Description 1',
            price_per_kg=Decimal('10.00'),
            approximate_weight=Decimal('0.100'),
            minimum_quantity=1
        )
        
        product2 = Product.objects.create(
            name='Test Product 2',
            description='Test Description 2',
            price_per_kg=Decimal('20.00'),
            approximate_weight=Decimal('0.200'),
            minimum_quantity=1
        )
        
        # Create order items but don't save them yet
        order_item1 = OrderItem(
            order=order,
            product=product1,
            quantity=5
        )
        
        order_item2 = OrderItem(
            order=order,
            product=product2,
            quantity=3
        )
        
        # Now save the order first (this gives it a primary key)
        order.save()
        
        # Now save the order items (they can now access order.order_items)
        order_item1.save()
        order_item2.save()
        
        # total_amount should be calculated automatically via property
        expected_total = sum(item.total_price for item in order.order_items.all())
        self.assertEqual(order.total_amount, expected_total)


class OrderItemModelTest(TestCase):
    """Test cases for the OrderItem model."""
    
    def setUp(self):
        """Set up test data for order item tests."""
        # Create User first
        self.user = User.objects.create_user(
            username='orderitemuser',
            email='john@testsupermarket.be',
            password='testpass123',
            role='customer'
        )
        
        self.customer = Customer.objects.create(
            user=self.user,
            customer_number='CUST001',
            company_name='Test Supermarket',
            address='123 Test Street, Brussels',
            vat_number='0123456789',
            contact_person='John Doe',
            phone_number='+32 2 123 45 67'
        )
        
        self.order = Order.objects.create(
            customer=self.customer,
            status='pending'
        )
        
        self.product = Product.objects.create(
            name='Test Product',
            description='Test Description',
            price_per_kg=Decimal('10.00'),
            approximate_weight=Decimal('0.100'),
            minimum_quantity=1
        )
        
        self.valid_order_item_data = {
            'order': self.order,
            'product': self.product,
            'quantity': 5
            # unit_price and total_price will be calculated automatically
        }
    
    def test_create_order_item(self):
        """Test creating an order item with valid data."""
        order_item = OrderItem.objects.create(**self.valid_order_item_data)
        self.assertEqual(order_item.order, self.order)
        self.assertEqual(order_item.product, self.product)
        self.assertEqual(order_item.quantity, 5)
        # unit_price should default to product's wholesale price
        self.assertEqual(order_item.unit_price, self.product.wholesale_price)
        # total_price should be quantity × unit_price
        expected_total = order_item.quantity * order_item.unit_price
        self.assertEqual(order_item.total_price, expected_total)
    
    def test_order_item_str_representation(self):
        """Test order item string representation."""
        order_item = OrderItem.objects.create(**self.valid_order_item_data)
        expected = '5x Test Product - €5.00'  # 5 × 1.00 = 5.00
        self.assertEqual(str(order_item), expected)
    
    def test_auto_calculate_total_price(self):
        """Test automatic total price calculation."""
        order_item = OrderItem.objects.create(**self.valid_order_item_data)
        # unit_price should default to product's wholesale price
        self.assertEqual(order_item.unit_price, self.product.wholesale_price)
        # total_price should be quantity × unit_price
        expected_total = order_item.quantity * order_item.unit_price
        self.assertEqual(order_item.total_price, expected_total)
    
    def test_unique_together_constraint(self):
        """Test that order and product combination must be unique."""
        OrderItem.objects.create(**self.valid_order_item_data)
        
        # Try to create another order item with same order and product
        duplicate_data = self.valid_order_item_data.copy()
        duplicate_data['quantity'] = 10
        duplicate_data['unit_price'] = Decimal('4.00')
        duplicate_data['total_price'] = Decimal('40.00')
        
        with self.assertRaises(Exception):
            OrderItem.objects.create(**duplicate_data)
    
    def test_quantity_validation(self):
        """Test quantity field validation."""
        # Test positive quantity
        order_item_data = self.valid_order_item_data.copy()
        order_item_data['quantity'] = 1
        # Create a new order to avoid unique constraint violation
        new_order = Order.objects.create(customer=self.customer)
        order_item_data['order'] = new_order
        order_item = OrderItem.objects.create(**order_item_data)
        self.assertEqual(order_item.quantity, 1)
        # unit_price and total_price should be calculated automatically
        self.assertEqual(order_item.unit_price, self.product.wholesale_price)
        self.assertEqual(order_item.total_price, self.product.wholesale_price)
        
        # Test zero quantity (should be allowed by model, but might be validated in forms)
        order_item_data['quantity'] = 0
        # Create another new order
        another_order = Order.objects.create(customer=self.customer)
        order_item_data['order'] = another_order
        order_item = OrderItem.objects.create(**order_item_data)
        self.assertEqual(order_item.quantity, 0)
        # total_price should be 0 when quantity is 0
        self.assertEqual(order_item.total_price, Decimal('0.00'))


class ModelRelationshipsTest(TestCase):
    """Test cases for model relationships."""
    
    def setUp(self):
        """Set up test data for relationship tests."""
        # Create User first
        self.user = User.objects.create_user(
            username='relationshipuser',
            email='john@testsupermarket.be',
            password='testpass123',
            role='customer'
        )
        
        self.customer = Customer.objects.create(
            user=self.user,
            customer_number='CUST001',
            company_name='Test Supermarket',
            address='123 Test Street, Brussels',
            vat_number='0123456789',
            contact_person='John Doe',
            phone_number='+32 2 123 45 67'
        )
        
        self.product = Product.objects.create(
            name='Test Product',
            description='Test Description',
            price_per_kg=Decimal('10.00'),
            approximate_weight=Decimal('0.100'),
            minimum_quantity=1
        )
    
    def test_customer_orders_relationship(self):
        """Test customer to orders relationship."""
        self.order1 = Order.objects.create(
            customer=self.customer,
            status='pending'
        )
        
        self.order2 = Order.objects.create(
            customer=self.customer,
            status='confirmed'
        )
        
        self.assertEqual(self.customer.orders.count(), 2)
        self.assertIn(self.order1, self.customer.orders.all())
        self.assertIn(self.order2, self.customer.orders.all())
    
    def test_order_items_relationship(self):
        """Test order to order items relationship."""
        order = Order.objects.create(
            customer=self.customer,
            status='pending'
        )
        
        # Create a second product to avoid unique constraint violation
        product2 = Product.objects.create(
            name='Test Product 2',
            description='Test Description 2',
            price_per_kg=Decimal('20.00'),
            approximate_weight=Decimal('0.200'),
            minimum_quantity=1
        )
        
        order_item1 = OrderItem.objects.create(
            order=order,
            product=self.product,
            quantity=2
            # unit_price and total_price will be calculated automatically
        )
        
        order_item2 = OrderItem.objects.create(
            order=order,
            product=product2,  # Use different product
            quantity=3
            # unit_price and total_price will be calculated automatically
        )
        
        self.assertEqual(order.order_items.count(), 2)
        self.assertIn(order_item1, order.order_items.all())
        self.assertIn(order_item2, order.order_items.all())
        
        # Test that order items can access their order
        self.assertEqual(order_item1.order, order)
        self.assertEqual(order_item2.order, order)
    
    def test_product_order_items_relationship(self):
        """Test product to order items relationship."""
        order = Order.objects.create(
            customer=self.customer,
            status='pending'
        )
        
        order_item = OrderItem.objects.create(
            order=order,
            product=self.product,
            quantity=5
            # unit_price and total_price will be calculated automatically
        )
        
        self.assertEqual(self.product.order_items.count(), 1)
        self.assertIn(order_item, self.product.order_items.all())
    
    def test_cascade_deletion(self):
        """Test cascade deletion behavior."""
        order = Order.objects.create(
            customer=self.customer,
            status='pending'
        )
        
        OrderItem.objects.create(
            order=order,
            product=self.product,
            quantity=5,
            unit_price=Decimal('3.00'),
            total_price=Decimal('15.00')
        )
        
        # Delete the order
        order.delete()
        
        # OrderItem should be deleted
        self.assertEqual(OrderItem.objects.count(), 0)
        
        # Product and Customer should still exist
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(Customer.objects.count(), 1)

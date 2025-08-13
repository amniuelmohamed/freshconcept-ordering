# Fresh Concept Ordering System

A Django-based B2B ordering platform for charcuterie wholesale distribution, designed to streamline operations between Fresh Concept and their diverse customer base.

## About Fresh Concept

Fresh Concept specializes in slicing, packaging, and distributing charcuterie products to:

-   **GMS (Grandes et Moyennes Surfaces)** - Supermarkets and retail chains *(Primary focus of this solution)*
-   **Food Service** - Restaurants, cafeterias, and catering companies *(Future expansion)*
-   **Industrial** - Food manufacturers requiring processing services *(Future expansion)*

## Project Overview

This web application addresses the unique needs of **GMS (Grandes et Moyennes Surfaces)** charcuterie distribution with customer-specific catalogs, flexible ordering systems, and comprehensive support features. The solution is designed specifically for supermarkets and retail chains, with future expansion possibilities to other customer types.

## Core Features

### Customer Management

-   **GMS-focused customer access** - Supermarkets and retail chains
-   Custom delivery schedules with JSON-based configuration
-   Order deadline validation and next delivery day calculation
-   Employee/admin-driven customer account creation

### Product Catalog

-   Automatic wholesale and retail price calculations
-   Margin rate management (default 30%)
-   VAT integration (6% Belgian VAT)
-   Minimum quantity enforcement
-   Standardized product weights and pricing per kilogram

### Order Processing

-   Order status management (pending, confirmed, cancelled)
-   Automatic total amount calculation from order items
-   Order item quantity and pricing management
-   Staff dashboard for order management (admin interface ready)

### Support System

-   Customer claims and quality issue reporting
-   Contact form with staff notification
-   Employee dashboard for support ticket management

### User Authentication

-   Custom User model with role-based access (customer, employee, admin)
-   Customer accounts managed by employees/admins
-   Password reset functionality (framework ready)
-   Role-based permission system

## Technical Implementation

### Built With

-   **Django 5.x** - Web framework
-   **Python 3.x** - Backend language
-   **SQLite** - Development database
-   **Django Admin** - Staff interface

### Key Django Concepts Implemented

-   **Custom User Model**: Extending AbstractUser with role-based authentication
-   **Model Relationships**: OneToOneField (User-Customer), ForeignKey (Order-Customer, OrderItem-Order/Product)
-   **Model Properties**: Computed fields for pricing calculations and business logic
-   **JSONField**: Flexible delivery schedule storage
-   **Model Validation**: Custom validators for VAT numbers and phone numbers
-   **Admin Customization**: ModelAdmin with custom display methods and fieldsets
-   **Testing**: Comprehensive test suite with proper test data isolation

### Architecture Decisions

-   **GMS-focused solution** - Designed specifically for supermarket and retail chain needs
-   Customer-specific delivery schedules (flexible over zone-based)
-   Standardized product catalog (consistent packaging and sizes)
-   Role-based access control (customer, employee, admin)
-   Integrated support ticket system

## Project Structure

```
freshconcept_ordering/
├── manage.py
├── freshconcept_ordering/
│   ├── settings.py          # Django settings with custom AUTH_USER_MODEL
│   ├── urls.py
│   └── wsgi.py
└── orders/
    ├── models.py            # User, Customer, Product, Order, OrderItem models
    ├── admin.py             # Customized admin interface
    ├── tests.py             # Comprehensive test suite
    ├── migrations/          # Database migrations
    ├── views.py
    ├── urls.py
    └── templates/
```

## Getting Started

### Prerequisites

-   Python 3.8+
-   pip
-   Virtual environment
-   Git (for cloning the repository)

### Installation

1. Clone the repository

```bash
git clone https://github.com/amniuelmohamed/freshconcept-ordering.git
cd freshconcept-ordering
```

2. Create and activate virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies

```bash
pip install django
```

4. Run migrations

```bash
python manage.py migrate
```

5. Create superuser

```bash
python manage.py createsuperuser
```

6. Run development server

```bash
python manage.py runserver
```

7. Run tests to verify everything works

```bash
python manage.py test
```

## Development Roadmap

### Phase 1: Core Foundation ✅

-   [x] Project setup and configuration
-   [x] Custom User model with role-based authentication (customer, employee, admin)
-   [x] Customer model with business logic and delivery schedules
-   [x] Product catalog with pricing calculations and variants
-   [x] Order and OrderItem models with relationships
-   [x] Django Admin customization for all models
-   [x] Comprehensive test suite for all models

### Phase 2: Ordering System

-   [x] Order model and relationships (Order, OrderItem with automatic pricing)
-   [ ] Shopping cart functionality
-   [ ] Order history and tracking
-   [ ] Delivery schedule integration (models ready, UI pending)

### Phase 3: Support Features

-   [ ] Claims/complaints system
-   [ ] Contact forms
-   [ ] Email notifications
-   [ ] Staff dashboard

### Phase 4: Advanced Features

-   [ ] Saved shopping lists
-   [ ] Bulk ordering tools
-   [ ] Reporting and analytics
-   [ ] API endpoints

## Learning Objectives

This project serves as a comprehensive Django learning experience covering:

-   **Model Design**: Complex business relationships, custom validators, and computed properties
-   **User Management**: Custom User model extending AbstractUser with role-based authentication
-   **Database Design**: OneToOneField, ForeignKey relationships, and unique constraints
-   **Admin Customization**: ModelAdmin with custom display methods, fieldsets, and search
-   **Testing**: Comprehensive test suite with proper test data isolation and constraint testing
-   **Business Logic**: Pricing calculations, delivery schedules, and order management

## Contributing

This is a learning project, but suggestions and feedback are welcome! Feel free to open issues or submit pull requests.

## License

This project is developed for educational purposes.

---

_Developing practical Django skills through real-world B2B application requirements._

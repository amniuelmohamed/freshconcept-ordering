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
-   **Bulk order form with validation and error display**
-   **Order modification vs. new order creation logic**

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

-   **Django 5.2.5** - Web framework
-   **Python 3.12** - Backend language
-   **PostgreSQL 16** - Production database (Docker)
-   **Redis 8** - Caching and sessions (Docker)
-   **Django Admin** - Staff interface
-   **Bootstrap 5.3** - Modern responsive UI

### Key Django Concepts Implemented

-   **Custom User Model**: Extending AbstractUser with role-based authentication
-   **Model Relationships**: OneToOneField (User-Customer), ForeignKey (Order-Customer, OrderItem-Order/Product)
-   **Model Properties**: Computed fields for pricing calculations and business logic
-   **JSONField**: Flexible delivery schedule storage
-   **Model Validation**: Custom validators for VAT numbers and phone numbers
-   **Admin Customization**: ModelAdmin with custom display methods and fieldsets
-   **Template System**: Template inheritance, custom filters, and Bootstrap integration
-   **View Logic**: Function-based views with authentication, form handling, and business logic
-   **URL Routing**: Named URLs, reverse lookups, and role-based redirects
-   **Testing**: Comprehensive test suite for models, views, and business logic
-   **Error Handling**: Professional error display with field-specific validation messages

### Architecture Decisions

-   **GMS-focused solution** - Designed specifically for supermarket and retail chain needs
-   Customer-specific delivery schedules (flexible over zone-based)
-   Standardized product catalog (consistent packaging and sizes)
-   Role-based access control (customer, employee, admin)
-   Integrated support ticket system
-   **Docker containerization** for consistent development and production environments

## Project Structure

```
freshconcept_ordering/
├── manage.py
├── requirements.txt          # Python dependencies
├── Dockerfile               # Docker container build
├── docker-compose.yml       # Multi-container orchestration
├── .env.example             # Environment variables template
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
    ├── templatetags/        # Custom template filters
    └── templates/
        ├── orders/          # Order-related templates
        └── registration/    # Authentication templates
```

## Getting Started

### Option 1: Docker (Recommended)

**Prerequisites:**
- Docker Desktop
- Git

**Quick Start:**
1. Clone the repository
```bash
git clone https://github.com/amniuelmohamed/freshconcept-ordering.git
cd freshconcept-ordering
```

2. Copy environment template and configure
```bash
cp .env.example .env
# Edit .env with your database credentials
```

3. Start the application
```bash
docker-compose up --build
```

4. Access the application
- **Main App**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin

5. Create superuser
```bash
docker-compose exec web python manage.py createsuperuser
```

### Option 2: Local Development

**Prerequisites:**
- Python 3.8+
- pip
- Virtual environment
- PostgreSQL (for production-like environment)

**Installation:**
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
pip install -r requirements.txt
```

4. Configure environment variables
```bash
cp .env.example .env
# Edit .env with your database credentials
```

5. Run migrations
```bash
python manage.py migrate
```

6. Create superuser
```bash
python manage.py createsuperuser
```

7. Run development server
```bash
python manage.py runserver
```

8. Run tests to verify everything works
```bash
python manage.py test
```

## Docker Configuration

### Services
- **Web**: Django application with Gunicorn
- **Database**: PostgreSQL 16 with persistent storage
- **Cache**: Redis 8 for sessions and caching

### Environment Variables
Copy `.env.example` to `.env` and configure:
- `DATABASE_URL`: PostgreSQL connection string
- `POSTGRES_DB`: Database name
- `POSTGRES_USER`: Database username
- `POSTGRES_PASSWORD`: Database password
- `DEBUG`: Development mode (set to 0 for production)

## Development Roadmap

### Phase 1: Core Foundation ✅

-   [x] Project setup and configuration
-   [x] Custom User model with role-based authentication (customer, employee, admin)
-   [x] Customer model with business logic and delivery schedules
-   [x] Product catalog with pricing calculations
-   [x] Order and OrderItem models with relationships
-   [x] Django Admin customization for all models
-   [x] Comprehensive test suite for all models

### Phase 2: Ordering System ✅

-   [x] Order model and relationships (Order, OrderItem with automatic pricing)
-   [x] Bulk order form with product catalog display
-   [x] Order modification vs. new order creation logic
-   [x] Delivery schedule integration with next delivery day calculation
-   [x] Order history display (last 3 orders with quantities)
-   [x] Order success page with order summary
-   [x] Role-based authentication and access control
-   [x] Comprehensive test suite for models and views
-   [x] **Professional error display system with field-specific validation**
-   [x] **Docker containerization with PostgreSQL and Redis**

**Next Steps for Phase 2:**
- [ ] Employee dashboard for managing products, customers, and orders
- [ ] Order status management (confirm/cancel orders)
- [ ] Customer order history and tracking
- [ ] Delivery schedule management interface

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

### Phase 5: Production Deployment

-   [ ] Production Docker configuration
-   [ ] SSL/HTTPS setup
-   [ ] Database backups and monitoring
-   [ ] CI/CD pipeline
-   [ ] Cloud deployment (AWS, Railway, etc.)

## Learning Objectives

This project serves as a comprehensive Django learning experience covering:

-   **Model Design**: Complex business relationships, custom validators, and computed properties
-   **User Management**: Custom User model extending AbstractUser with role-based authentication
-   **Database Design**: OneToOneField, ForeignKey relationships, and unique constraints
-   **Admin Customization**: ModelAdmin with custom display methods, fieldsets, and search
-   **Template System**: Template inheritance, custom filters, and modern UI with Bootstrap
-   **View Logic**: Function-based views with authentication, form handling, and business logic
-   **URL Routing**: Named URLs, reverse lookups, and role-based redirects
-   **Testing**: Comprehensive test suite for models, views, and business logic
-   **Business Logic**: Pricing calculations, delivery schedules, order management, and GMS workflows
-   **Docker & DevOps**: Containerization, multi-service orchestration, and production deployment
-   **Error Handling**: Professional user experience with clear validation feedback

## Contributing

This is a learning project, but suggestions and feedback are welcome! Feel free to open issues or submit pull requests.

## License

This project is developed for educational purposes.

---

_Developing practical Django skills through real-world B2B application requirements._

# Fresh Concept Ordering System

A Django-based B2B ordering platform for charcuterie wholesale distribution, designed to streamline operations between Fresh Concept and their diverse customer base.

## About Fresh Concept

Fresh Concept specializes in slicing, packaging, and distributing charcuterie products to:

-   **GMS (Grandes et Moyennes Surfaces)** - Supermarkets and retail chains
-   **Food Service** - Restaurants, cafeterias, and catering companies
-   **Industrial** - Food manufacturers requiring processing services

## Project Overview

This web application addresses the unique needs of B2B charcuterie distribution with customer-specific catalogs, flexible ordering systems, and comprehensive support features.

## Core Features

### Customer Management

-   Multi-tier customer access (GMS, Food Service, Industrial)
-   Custom delivery schedules and order deadlines
-   Automated account creation with email notifications

### Product Catalog

-   Customer-specific product visibility
-   Multiple packaging formats per product
-   Minimum quantity enforcement
-   Saved items for frequent orders

### Order Processing

-   Order history and tracking
-   Delivery schedule integration
-   Staff dashboard for order management

### Support System

-   Customer claims and quality issue reporting
-   Contact form with staff notification
-   Employee dashboard for support ticket management

### User Authentication

-   Secure login/logout system
-   Password reset functionality
-   Role-based access control

## Technical Implementation

### Built With

-   **Django 5.x** - Web framework
-   **Python 3.x** - Backend language
-   **SQLite** - Development database
-   **Django Admin** - Staff interface

### Key Django Concepts Implemented

-   Custom User models and authentication
-   Complex model relationships (Foreign Keys, Many-to-Many)
-   Form handling and validation
-   Email automation
-   Permission-based views
-   Custom Django Admin interface

### Architecture Decisions

-   Customer-specific delivery schedules (flexible over zone-based)
-   Product variants system (same product, different packaging)
-   Hierarchical customer access levels
-   Integrated support ticket system

## Project Structure

```
freshconcept_ordering/
├── manage.py
├── freshconcept_ordering/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── orders/
    ├── models.py
    ├── views.py
    ├── urls.py
    └── templates/
```

## Getting Started

### Prerequisites

-   Python 3.8+
-   pip
-   Virtual environment

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

## Development Roadmap

### Phase 1: Core Foundation ✅

-   [x] Project setup and configuration
-   [ ] Customer model with business logic
-   [ ] Product catalog with variants
-   [ ] Basic authentication system

### Phase 2: Ordering System

-   [ ] Order model and relationships
-   [ ] Shopping cart functionality
-   [ ] Order history and tracking
-   [ ] Delivery schedule integration

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

-   **Model Design**: Complex business relationships and data validation
-   **User Management**: Custom authentication and permission systems
-   **Form Processing**: Dynamic forms with business rule validation
-   **Admin Customization**: Tailored staff interfaces
-   **Email Integration**: Automated business communications
-   **Security**: Role-based access and data protection

## Contributing

This is a learning project, but suggestions and feedback are welcome! Feel free to open issues or submit pull requests.

## License

This project is developed for educational purposes.

---

_Developing practical Django skills through real-world B2B application requirements._

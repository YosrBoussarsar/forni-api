# Forni Bakery API

A comprehensive REST API for managing a bakery's online ordering system built with Flask.

## Features

- User authentication (register, login, logout)
- Role-based access control (admin, baker, client)
- Product management
- Order management
- Review system
- JWT-based authentication

## Setup

### Prerequisites

- Python 3.8+
- PostgreSQL (optional, SQLite is used by default)

### Installation

1. Create and activate virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # On Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create `.env` file from `.env.example`:
```bash
copy .env.example .env
```

4. Update `.env` with your configuration

5. Initialize database:
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

6. Run the application:
```bash
python run.py
```

The API will be available at `http://localhost:5000`

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `POST /api/auth/logout` - Logout user
- `POST /api/auth/refresh` - Refresh access token
- `GET /api/auth/profile` - Get user profile
- `PUT /api/auth/profile` - Update user profile

### Products
- `GET /api/products` - List all products
- `POST /api/products` - Create product (admin/baker only)
- `GET /api/products/<id>` - Get product details
- `PUT /api/products/<id>` - Update product (admin/baker only)
- `DELETE /api/products/<id>` - Delete product (admin only)

### Orders
- `GET /api/orders` - List orders
- `POST /api/orders` - Create new order
- `GET /api/orders/<id>` - Get order details
- `PUT /api/orders/<id>` - Update order status (admin/baker only)
- `DELETE /api/orders/<id>` - Cancel order

### Reviews
- `GET /api/reviews` - List reviews
- `POST /api/reviews` - Create review
- `PUT /api/reviews/<id>` - Update review
- `DELETE /api/reviews/<id>` - Delete review

## Database Models

- **User**: User accounts with role-based access
- **Product**: Bakery products catalog
- **Order**: Customer orders
- **OrderItem**: Individual items in orders
- **Review**: Product reviews and ratings

## Technologies

- Flask - Web framework
- SQLAlchemy - ORM
- Flask-JWT-Extended - JWT authentication
- Flask-RESTful - REST API framework
- Marshmallow - Serialization/validation
- Flask-Bcrypt - Password hashing
- Flask-CORS - CORS support

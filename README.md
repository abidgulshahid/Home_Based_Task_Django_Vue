# E-commerce API with Django and Vue

A full-stack e-commerce application with Django REST Framework backend and Vue.js frontend.

## Features

- Product and Category management
- RESTful API endpoints
- Custom search and filtering
- Bulk operations
- Raw SQL queries for specific operations
- Vue.js frontend with basic CRUD operations

## Prerequisites

- Python 3.8+
- Node.js 14+
- npm or yarn
- SQLite (development) or PostgreSQL (production)

## Backend Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd ecommerce
```

2. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up the database:
```bash
./reset_db.sh
```

5. Run the development server:
```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/`

## API Endpoints

- `GET /api/products/` - List all products
- `POST /api/products/` - Create a new product
- `GET /api/products/{id}/` - Get product details
- `PUT /api/products/{id}/` - Update a product
- `DELETE /api/products/{id}/` - Delete a product
- `GET /api/products/low_stock/` - Get products with low stock
- `POST /api/products/bulk_update_stock/` - Bulk update product stock
- `GET /api/categories/` - List all categories
- `POST /api/categories/` - Create a new category

## Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Run the development server:
```bash
npm run serve
```

The frontend will be available at `http://localhost:8080`

## Development Scripts

- `./setup.sh` - Initial project setup
- `./reset_db.sh` - Reset database and load sample data
- `python load_sample_data.py` - Load sample data

## Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.

## Security Considerations

1. Always use HTTPS in production
2. Keep dependencies updated
3. Use strong passwords
4. Implement rate limiting
5. Regular security audits

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
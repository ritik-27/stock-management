# Stock Management API

A Flask-based REST API for managing product inventory with automatic restock detection. This application provides comprehensive CRUD operations for products and intelligent restock management based on configurable thresholds.

## Features

- **CRUD operations for Products**
- **Automatic Restock Detection**
- **RESTful API Design**
- **Input Validation and Error handling**

## Tech Stack

- **Python 3.x**
- **Flask 2.3.3**
- **MongoEngine** 
- **MongoDB**

## Prerequisites

- Python 3.7 or higher
- MongoDB (local installation or MongoDB Atlas)
- pip (Python package manager)

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/ritik-27/stock-management.git
cd stock-management
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy the `.env.example` file to `.env` and update the values as needed:

```bash
cp .env.example .env
```

### 5. Start MongoDB

Ensure MongoDB is running on your system:

```bash
# If using local MongoDB
mongod
```

Or use MongoDB Atlas connection string in `.env`.

### 6. Run the Application

```bash
python run.py
```

The API will be available at `http://localhost:5000`

## API Documentation

### Base URL
```
http://localhost:5000
```

### Endpoints

---

#### 1. Create Product

**Endpoint:** `POST /product`

**Description:** Creates a new product in the inventory.

**Request Body:**
```json
{
  "name": "Laptop",
  "description": "High-performance laptop",
  "price": 999.99,
  "total_quantity": 100,
  "available_quantity": 85
}
```

**Response:** `201 Created`
```json
{
  "id": "507f1f77bcf86cd799439011",
  "name": "Laptop",
  "description": "High-performance laptop",
  "price": 999.99,
  "total_quantity": 100,
  "available_quantity": 85,
  "need_restock": false
}
```

**Error Responses:**
- `400 Bad Request`: Invalid data types or missing required fields
- `400 Bad Request`: Validation error

---

#### 2. Get All Products

**Endpoint:** `GET /product`

**Description:** Retrieves a list of all products in the inventory.

**Response:** `200 OK`
```json
[
  {
    "id": "507f1f77bcf86cd799439011",
    "name": "Laptop",
    "description": "High-performance laptop",
    "price": 999.99,
    "total_quantity": 100,
    "available_quantity": 85,
    "need_restock": false
  },
  {
    "id": "507f1f77bcf86cd799439012",
    "name": "Mouse",
    "description": "Wireless mouse",
    "price": 29.99,
    "total_quantity": 50,
    "available_quantity": 5,
    "need_restock": true
  }
]
```

---

#### 3. Get Product by ID

**Endpoint:** `GET /product/<product_id>`

**Description:** Retrieves a specific product by its ID.

**Path Parameters:**
- `product_id` (string): MongoDB ObjectId of the product

**Response:** `200 OK`
```json
{
  "id": "507f1f77bcf86cd799439011",
  "name": "Laptop",
  "description": "High-performance laptop",
  "price": 999.99,
  "total_quantity": 100,
  "available_quantity": 85,
  "need_restock": false
}
```

**Error Responses:**
- `404 Not Found`: Product not found

---

#### 4. Update Product

**Endpoint:** `PUT /product/<product_id>`

**Description:** Updates an existing product. Only provided fields will be updated.

**Path Parameters:**
- `product_id` (string): MongoDB ObjectId of the product

**Request Body:** (all fields optional)
```json
{
  "name": "Updated Laptop",
  "description": "Updated description",
  "price": 899.99,
  "total_quantity": 120,
  "available_quantity": 100
}
```

**Updatable Fields:**
- `name` (string)
- `description` (string)
- `price` (float)
- `total_quantity` (integer)
- `available_quantity` (integer)

**Note:** If `available_quantity` exceeds `total_quantity`, it will be automatically adjusted. The `need_restock` flag is automatically calculated based on the threshold.

**Response:** `200 OK`
```json
{
  "id": "507f1f77bcf86cd799439011",
  "name": "Updated Laptop",
  "description": "Updated description",
  "price": 899.99,
  "total_quantity": 120,
  "available_quantity": 100,
  "need_restock": false
}
```

**Error Responses:**
- `400 Bad Request`: Invalid data types or no valid fields provided
- `400 Bad Request`: available_quantity cannot be greater than total_quantity
- `404 Not Found`: Product not found

---

#### 5. Delete Product

**Endpoint:** `DELETE /product/<product_id>`

**Description:** Deletes a product from the inventory.

**Path Parameters:**
- `product_id` (string): MongoDB ObjectId of the product

**Response:** `200 OK`
```json
{
  "message": "Product deleted"
}
```

**Error Responses:**
- `404 Not Found`: Product not found

---

#### 6. Check Restock Status

**Endpoint:** `GET /restock/<product_id>`

**Description:** Checks if a specific product needs restocking.

**Path Parameters:**
- `product_id` (string): MongoDB ObjectId of the product

**Response:** `200 OK`
```json
{
  "id": "507f1f77bcf86cd799439011",
  "need_restock": true,
  "available_quantity": 15,
  "total_quantity": 100
}
```

**Error Responses:**
- `404 Not Found`: Product not found

---

#### 7. Update Restock Status Manually

**Endpoint:** `PUT /restock/update/<product_id>`

**Description:** Manually updates the restock flag for a product (overrides automatic calculation).

**Path Parameters:**
- `product_id` (string): MongoDB ObjectId of the product

**Request Body:**
```json
{
  "need_restock": true
}
```

**Required Fields:**
- `need_restock` (boolean): true or false


**Response:** `200 OK`
```json
{
  "id": "507f1f77bcf86cd799439011",
  "name": "Laptop",
  "description": "High-performance laptop",
  "price": 999.99,
  "total_quantity": 100,
  "available_quantity": 85,
  "need_restock": true
}
```

**Error Responses:**
- `400 Bad Request`: Invalid data or missing required field
- `404 Not Found`: Product not found

---

#### 8. List All Products Needing Restock

**Endpoint:** `GET /restock/list`

**Description:** Retrieves all products that are flagged as needing restock.

**Response:** `200 OK`
```json
[
  {
    "id": "507f1f77bcf86cd799439012",
    "name": "Mouse",
    "description": "Wireless mouse",
    "price": 29.99,
    "total_quantity": 50,
    "available_quantity": 5,
    "need_restock": true
  },
  {
    "id": "507f1f77bcf86cd799439013",
    "name": "Keyboard",
    "description": "Mechanical keyboard",
    "price": 79.99,
    "total_quantity": 30,
    "available_quantity": 3,
    "need_restock": true
  }
]
```

---

## Restock Logic

Products are automatically flagged for restock when `available_quantity < (total_quantity × RESTOCK_THRESHOLD)`. Default threshold is 20%.

## Project Structure

```
stock-management/
├── app/
│   ├── __init__.py           
│   ├── models.py             
│   ├── utils.py              
│   └── routes/
│       └── product_routes.py 
├── config.py                 
├── run.py                    
├── requirements.txt          
├── .env                      
└── README.md             
```

# 🍽️ Recipe Management System

A complete web application for managing and sharing recipes built with Python Flask, SQLite, and modern web technologies.

## 📋 Table of Contents
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Database Schema](#database-schema)
- [Usage](#usage)
- [API Routes](#api-routes)

## ✨ Features

- 🔐 **User Authentication** - Secure login system with password hashing
- 📚 **Recipe Categories** - Organized by Salads, Lunch, Main Dishes, Breakfast, Fast Foods
- 🖼️ **Image Upload** - Store recipe images directly in database
- 💬 **Comment System** - Users can comment on recipes
- ➕ **Add Recipes** - Intuitive form for adding new recipes
- 🗑️ **Delete Recipes** - Easy recipe management
- 📱 **Responsive Design** - Works on desktop and mobile devices
- 🔍 **Search Functionality** - Find recipes quickly
- 🎨 **Modern UI** - Beautiful gradient backgrounds and animations

## 🛠 Technology Stack

### Backend
- **Python 3** - Core programming language
- **Flask** - Web framework
- **SQLite** - Database management
- **DB Browser for SQLite** - Database visualization
- **Hashlib** - Password encryption

### Frontend
- **HTML5** - Page structure
- **CSS3** - Styling with gradients and animations
- **JavaScript** - Modal interactions
- **Bootstrap** - UI components (Login page)

### Database
- **SQLite** - Lightweight relational database
- **BLOB Storage** - Recipe images stored as binary data

## 📁 Project Structure

```
recipe-app/
│
├── app.py                 # Main Flask application
├── recipes.db            # SQLite database (created automatically)
│
├── templates/            # HTML templates
│   ├── login.html        # User login page
│   ├── index.html        # Main dashboard with categories
│   ├── category.html     # Recipes by category
│   └── recipe.html       # Individual recipe details
│
└── static/
    └── no_image.jpg      # Default image for recipes
```

## 🚀 Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Step-by-Step Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd recipe-app
   ```

2. **Create virtual environment (recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install required packages**
   ```bash
   pip install flask
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the application**
   Open your browser and go to: `http://127.0.0.1:5000`

## 🗃️ Database Schema

The application uses 4 main tables:

### Categories Table
```sql
CREATE TABLE categories (
    id INTEGER PRIMARY KEY,
    name TEXT
);
```

### Recipes Table
```sql
CREATE TABLE recipes (
    id INTEGER PRIMARY KEY,
    category_id INTEGER,
    name TEXT,
    ingredients TEXT,
    instructions TEXT,
    dish_image BLOB,
    FOREIGN KEY(category_id) REFERENCES categories(id)
);
```

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);
```

### Comments Table
```sql
CREATE TABLE comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    recipe_id INTEGER NOT NULL,
    user_name TEXT NOT NULL,
    comment_text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(recipe_id) REFERENCES recipes(id) ON DELETE CASCADE,
    CHECK(length(comment_text) <= 500)
);
```

## 👥 Default Users

The application comes with pre-configured users:

| Username | Password | Role |
|----------|----------|------|
| admin | admin | Administrator |
| shreyash | shreyashguptacdac | User |
| shivam | shivam | User |

**Note:** Passwords are securely hashed using SHA-256 encryption.

## 📊 Usage Guide

### 1. Login
- Navigate to the login page
- Enter username and password
- Successful login redirects to main dashboard

### 2. Browse Categories
- View all recipe categories on the main page
- Click any category to see recipes in that category

### 3. View Recipes
- Click on any recipe name to view details
- See ingredients, instructions, and image
- Read and post comments

### 4. Add New Recipe
- Click the `+` floating button
- Fill in recipe details
- Upload an image
- Select category
- Submit to add to database

### 5. Delete Recipes
- Click the `🗑️` floating button
- Enter exact recipe name
- Confirm deletion

### 6. Comment on Recipes
- Navigate to any recipe page
- Scroll to comment section
- Write and post comments
- View comment history

## 🌐 API Routes

| Route | Method | Description | Authentication |
|-------|--------|-------------|----------------|
| `/` | GET | Redirects to login | No |
| `/login` | GET, POST | User login | No |
| `/index` | GET | Main dashboard | Required |
| `/logout` | GET | User logout | Required |
| `/category/<id>` | GET | Show recipes by category | Required |
| `/recipe/<id>` | GET | Show recipe details | Required |
| `/add_recipe` | POST | Add new recipe | Required |
| `/delete_recipe` | POST | Delete recipe | Required |
| `/add_comment/<id>` | POST | Add comment to recipe | Required |
| `/recipe_image/<id>` | GET | Serve recipe image | No |


## 🔧 Database Management with DB Browser

### Viewing Data
1. Install [DB Browser for SQLite](https://sqlitebrowser.org/)
2. Open `recipes.db` file
3. Browse tables in "Browse Data" tab
4. View images stored as BLOB data

### Manual Database Operations
You can manually:
- Add new categories
- View user accounts
- Export recipe data
- Backup the database

## 🎨 Customization

### Adding New Categories
Edit the database directly or modify the `init_db()` function in `app.py` to include new categories.

### Styling Changes
Modify CSS in respective HTML files:
- `index.html` - Main dashboard styling
- `login.html` - Login page styling  
- `category.html` - Category page styling
- `recipe.html` - Recipe detail page styling

### Adding New Features
The modular Flask structure makes it easy to:
- Add user registration
- Implement recipe ratings
- Add recipe search filters
- Include social sharing


## 👨‍💻 CONTRIBUTORS

**THE EAGLES**
- PG-DBDA AUG-2025

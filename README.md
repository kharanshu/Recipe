## Steps to run this project on Windows

set FLASK_APP=run.py

# To Do DB Migrations
flask db init 
flask db migrate -m "Initial migration"
flask db upgrade

# TO run flask server 
flask run

# Addition Installation of Packages
python -m pip install --upgrade pip
pip install -r requirements.txt 


# Server Run on http://127.0.0.1:5000 

# URL End Points included in this application

/home - Initial Home Page
/register - New User Registration Form
/login - Login Form
/logout - Logout Page
/recipe/new - Form to add new recipe
/recipe/recipe_id - To view recipe with its known ID
/recipe/recipe_id/edit - Form to edit Existing recipe with help of ID
/recipe/recipe_id/delete - Form to delete existing recipe with recipe ID

# Project Structure
RECIPES/
│
├── app/
│   ├── __init__.py        # Application initialization
│   ├── models.py          # SQLAlchemy models (User, Recipe)
│   ├── routes.py          # Flask routes (authentication, CRUD endpoints)
│   ├── forms.py           # Flask-WTF forms (for input validation)
│   ├── templates/         # HTML templates
│   │   ├── base.html      # Base template (header, footer)
│   │   ├── login.html     # Login form template
│   │   ├── home.html      # Dashboard template
│   │   ├── recipe/        # Recipe-related templates
│   │   │   ├── recipe_form.html   # Create recipe form template
│   │   │   ├── edit_recipe.html   # Update recipe form template
│   └── tests/             # Unit tests
│       └── test_routes.py # Test cases for routes and functionality
│
├── migrations/            # Database migrations (if using Flask-Migrate)
│
├── config.py              # Configuration settings (database URI, secret key, etc.)
├── run.py                 # Entry point to run the Flask application
└── requirements.txt       # Python dependencies



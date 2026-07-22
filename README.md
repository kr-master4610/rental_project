# Rental Project (Property Rental API & Web)

## 📌 Project Overview
A comprehensive web application and RESTful API built with **Django** and **Django REST Framework (DRF)** for managing real estate listings, user authentication, bookings, reviews, and search/view history. 

Designed to support both a traditional server-rendered frontend and a robust API backend.

---

## 🛠 Tech Stack
* **Backend:** Python, Django, Django REST Framework (DRF)
* **Authentication:** JWT (JSON Web Tokens), Django Session Auth
* **Filtering & Search:** `django-filter`, DRF SearchFilter & OrderingFilter
* **Documentation:** `drf-spectacular` (OpenAPI / Swagger UI)
* **Database:** SQLite / PostgreSQL (via Docker)
* **Frontend:** HTML5, CSS3, Django Templates

---

## 🚀 Key Features
1. **Listings Management:** Landlords can create, update, and manage property listings (Title, Price, Location, Rooms, Housing Type). Public users can view active listings and search/filter them.
2. **Role-Based Permissions:** Custom permissions (`IsLandlordOrReadOnly`) ensuring only property owners can modify their listings.
3. **REST API & Swagger:** Fully documented endpoints with automatic OpenAPI schema generation.
4. **User Tracking:** Automatic logging of user search queries and listing view history.
5. **Web & API Hybrid:** Supports standard browser navigation/forms alongside token-authenticated API endpoints.

---

## ⚙️ Installation & Running

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd rental_project
   Create and activate a virtual environment:

Bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
Install dependencies:

Bash
pip install -r requirements.txt
Apply database migrations:

Bash
python manage.py makemigrations
python manage.py migrate
Run the development server:

Bash
python manage.py runserver
Access the application:

Web Frontend: http://127.0.0.1:8000/

API Documentation (Swagger): http://127.0.0.1:8000/api/docs/
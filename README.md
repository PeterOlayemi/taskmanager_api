# TaskManager API

A Django RESTful API for managing tasks with JWT authentication. Users can register, log in, create tasks, assign tasks to other users, and update task statuses. The API enforces role-based permissions for owners and assignees.

## Features
- User registration and JWT authentication
- Create, retrieve, update, and delete tasks
- Assign tasks to other users
- Only the assignee can update the task status
- Clean, modular code structure
- Logical database design

## Tech Stack
- Python 3
- Django 5
- Django REST Framework
- SimpleJWT (for JWT authentication)
- SQLite (default, can be changed)

## Setup Instructions

### 1. Clone the repository
```
git clone https://github.com/PeterOlayemi/taskmanager_api.git
cd taskmanager_api
```

### 2. Create and activate a virtual environment (recommended)
```
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies
```
pip install -r requirements.txt
```

### 4. Set up environment variables
Create a `.env` file in the root directory with at least:
```
SECRET_KEY=your-django-secret-key
```

### 5. Apply migrations
```
python manage.py migrate
```

### 6. Create a superuser (optional, for admin access)
```
python manage.py createsuperuser
```

### 7. Run the development server
```
python manage.py runserver
```

## API Endpoints

| Endpoint                        | Method | Description                        |
|---------------------------------|--------|------------------------------------|
| `/api/auth/register/`           | POST   | Register a new user                |
| `/api/auth/token/`              | POST   | Obtain JWT access/refresh tokens   |
| `/api/auth/token/refresh/`      | POST   | Refresh JWT access token           |
| `/api/tasks/`                   | GET    | List tasks (owner/assignee)        |
| `/api/tasks/`                   | POST   | Create a new task                  |
| `/api/tasks/{id}/`              | GET    | Retrieve a task                    |
| `/api/tasks/{id}/`              | PUT    | Update a task (owner only)         |
| `/api/tasks/{id}/`              | DELETE | Delete a task (owner only)         |
| `/api/tasks/{id}/assign/`       | POST   | Assign a user to a task (owner)    |
| `/api/tasks/{id}/status/`       | PATCH  | Update status (assignee only)      |

### Authentication
All endpoints (except registration and token obtain/refresh) require a JWT Bearer token in the `Authorization` header:
```
Authorization: Bearer <access_token>
```

## Postman Collection
A ready-to-use Postman collection is provided: `taskmanager_postman_collection.json`.
- Import it into Postman to test all endpoints.
- Set the `base_url` variable (default: `http://localhost:8000`).
- Use the collection variables for `access_token`, `refresh_token`, etc.

## Testing
To run tests (add your own in `tasks/tests.py`):
```
python manage.py test
```

## License
[MIT](LICENSE) (or your preferred license)

---

**Author:** Peter Olayemi

For questions or contributions, please open an issue or pull request.

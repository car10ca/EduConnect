# EduConnect

EduConnect is a modern e-learning platform built with Django. It enables seamless interaction between **students** and **teachers**, offering features like course enrollment, real-time chat, notifications, and structured learning flows.

---

## ✨ Features

- **User Roles**: Supports two account types - Students and Teachers  
- **Course Management**: Teachers can create, edit, and manage course content  
- **Enrollment System**: Students can enroll or unenroll from courses  
- **Notifications**: Real-time updates on enrollment changes  
- **Chat Functionality**: Instant messaging between users  
- **RESTful API**: Easily accessible API endpoints for frontend or mobile apps  
- **Asynchronous Tasks**: Handled via Celery & Redis for notifications and background processing  
- **Testing Suite**: Includes unit tests for views, models, and APIs  

---

## 🧰 Tech Stack

- **Backend**: Django 5.1  
- **Database**: PostgreSQL  
- **Asynchronous Handling**: Django Channels, Redis, Celery  
- **API**: Django REST Framework (DRF)  
- **Chat & Notifications**: Channels + WebSockets  

---

## ⚙️ Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/educonnect.git
cd educonnect

2. **Create virtual environment & activate it**
```python -m venv env
source env/bin/activate```  # On Windows: env\Scripts\activate

3. **Install dependencies**
pip install -r requirements.txt

4. **Set up your environment variables**
Create a .env file in the root directory and configure your database and Redis URLs:

```SECRET_KEY=your_django_secret
DEBUG=True
DATABASE_URL=postgres://user:password@localhost:5432/educonnect_db
REDIS_URL=redis://localhost:6379```

5. **Apply migrations & create superuser**
```python manage.py migrate
python manage.py createsuperuser```

6. **Run the development server**
```python manage.py runserver```

7. **Run Celery worker (in another terminal)```**
```celery -A educonnect worker -l info```


8. **Run Redis server (make sure it's installed and running)**
```redis-server```


## 📊 API Endpoints (sample)
Method	Endpoint	Description
GET	/api/courses/	List all courses
POST	/api/enroll/	Enroll a student into a course
DELETE	/api/unenroll/	Unenroll a student
GET	/api/notifications/	Get user notifications
Full API documentation coming soon!

## ✅ Running Tests
pytest

## 📄 License
This project is open source under the MIT License.

## 🚀 Future Improvements
- Video streaming integration
- Progress tracking dashboard for students


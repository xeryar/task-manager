# 🌟 Django Task Management System 🌟

Welcome to the **Django Task Management System**!  
This project is a **modern, efficient, and robust task management platform** designed to streamline task handling, scheduling, and approvals using **Redis** and **Celery**.  

---

## 🚀 Features
- **Task Management**: Create, update, approve, and schedule tasks.
- **Approval Workflow**: Tasks pending approval are handled efficiently with delayed saves.
- **Scheduling**: Automatically manage and delete old tasks using Celery and Redis.
- **Role-Based Access**: Secure access control based on user roles.
- **Modern Architecture**: Fully integrated with Redis for caching and Celery for task queuing.

---

## 🛠️ Technologies Used
- **Python** (Django Framework)
- **Redis** (Cache & Task Queue)
- **Celery** (Task Scheduling)
- **MySQL** (Database)

---


## 🖥️ Setup Instructions

Before proceeding to setup kindly create the .env file in the project and set values according to the .env.sample
Follow the steps below to set up and run the project locally:

### 1️⃣ Create and Activate Virtual Environment
```bash
py -m venv venv
.\venv\Scripts\activate
```

### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Create or reset the Database
Run the custom command to create or reset the database:
```bash
.\commands\reset_db.py
```

### 4️⃣ Start Redis Server
Ensure Redis is running in the background:
```bash
redis-server
```

### 5️⃣ Start Celery Worker
Run the Celery worker to handle asynchronous tasks:
```bash
celery -A core worker --pool=solo --loglevel=info
```

### 6️⃣ Start Celery Beat
Start Celery Beat for periodic task scheduling:
```bash
celery -A core beat --loglevel=info
```

### 7️⃣ Run Task Deletion Scheduler
Initiate the scheduler for deleting old tasks:
```bash
py manage.py run_task_deletion_scheduler
```

### 8️⃣ Run the Django Server
Start the Django development server:
```bash
py manage.py runserver
```

---

## 🌐 How to Use the Application
1. **Log In**: Authenticate with your credentials.
2. **Manage Tasks**: 
   - Add new tasks.
   - View tasks pending approval.
   - Approve or disapprove tasks.
3. **Scheduled Task Deletion**:
   - Tasks marked as "completed" for over 2 days are automatically removed weekly.
4. **Role-Based Access**: Actions are restricted based on user roles.

---

## 🧰 Development Tools
### Recommended Tools:
- **Visual Studio Code**: For code editing.
- **Postman**: For testing APIs.

---

## 📬 Contact
For queries or feedback, feel free to reach out:  
📧 Email: **sheryarbaloch67@gmail.com**

---

**✨ Thank you for using the Django Task Management System! ✨**
```
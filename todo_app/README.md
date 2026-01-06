# Smart To-Do App

A Flask-based to-do list application with time tracking and status management.

## Features
- Add tasks with time estimates (hours, days, months)
- Automatic status updates (Pending, Overdue, Completed)
- Responsive design with Bootstrap
- Real-time time remaining calculations

## Local Development
1. Install dependencies: `pip install -r requirements.txt`
2. Run the app: `python app.py`
3. Open `http://127.0.0.1:5000/`

## Deployment to Render
1. Push this code to a GitHub repository
2. Go to [Render.com](https://render.com) and sign up/login
3. Click "New +" and select "Web Service"
4. Connect your GitHub repository
5. Configure the service:
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
6. Click "Create Web Service"

Your app will be live at the provided Render URL!
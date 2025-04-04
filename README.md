# 📧 Flask + React Email Submission System

A full-stack email submission system using **Flask (Python)** for the backend and **React** for the frontend. This project allows users to submit messages via a contact form, which are then emailed using **Gmail SMTP** and stored in a database.

## 🚀 Features
- ✅ Send emails via a contact form using **Gmail SMTP**
- ✅ Store submissions in a **PostgreSQL database**
- ✅ Full **CRUD** operations on submissions
- ✅ Secure **user authentication** (optional)
- ✅ **React frontend** with a modern UI

## 🛠️ Technologies Used

### Backend (Flask)
- Flask
- Flask-CORS
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-RESTful
- SMTP (Gmail)
- PostgreSQL
- Gunicorn

### Frontend (React)
- React (Vite)
- Axios
- Tailwind CSS
- React Hook Form

## 📂 Project Structure

```
flask-gmail-smtp/
├── backend/
│   ├── app.py
│   ├── models.py
│   ├── config.py
│   ├── routes.py
│   ├── migrations/
│   ├── .env
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── App.jsx
│   │   └── index.js
│   ├── package.json
│   ├── tailwind.config.js
│   └── vite.config.js
│
└── README.md
```

## 🖥️ Backend Setup

1. **Clone the Repository**
```bash
git clone https://github.com/your-username/flask-gmail-smtp.git
cd flask-gmail-smtp/backend
```

2. **Create Virtual Environment**
```bash
pip install pipenv
pipenv shell
pipenv install
```

3. **Configure Environment**
Create `.env` file:
```bash
EMAIL_ADDRESS=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
DATABASE_URL=postgresql://user:password@localhost:5432/db_name
```

4. **Initialize Database**
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

5. **Run Development Server**
```bash
flask run
```

## 🎨 Frontend Setup

1. **Install Dependencies**
```bash
cd frontend
npm install
```

2. **Start Development Server**
```bash
npm run dev
```

## 🔥 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/submissions` | Get all submissions |
| POST | `/send-email` | Send an email |
| GET | `/submissions/:id` | Get single submission |
| PUT | `/submissions/:id` | Update submission |
| PATCH | `/submissions/:id` | Partial update |
| DELETE | `/submissions/:id` | Delete submission |

## 🚀 Deployment

### Backend
```bash
gunicorn -w 4 app:app
```

### Frontend
- Deploy to Vercel or Netlify
- Update API URL in environment configuration

## 📝 Notes
- Keep `.env` and `config.py` out of version control
- Use environment variables for sensitive data
- Manage dependencies with pipenv

## 💡 Future Improvements
- [ ] User authentication (JWT/OAuth)
- [ ] HTML email templates
- [ ] Admin dashboard

## 📜 License
MIT

---
Built with ❤️ using Flask & React.
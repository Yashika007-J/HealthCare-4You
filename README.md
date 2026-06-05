# HealthCare-4You

# 🩺 HealthCare Assistant Chatbot

An AI-powered Healthcare Assistant Chatbot built using Flask, Python, HTML, CSS, and JavaScript. The application helps users access basic health information, calculate BMI, and interact with an intelligent chatbot powered by the Gemini API.

## Features

### AI Health Chatbot
- Provides health-related information and guidance.
- Uses Google Gemini API for intelligent and context-aware responses.
- User-friendly chat interface.

### BMI Calculator
- Calculates Body Mass Index (BMI) using user height and weight.
- Displays BMI category:
  - Underweight
  - Normal Weight
  - Overweight
  - Obese

### User Authentication
- Secure user registration and login system.
- Password hashing for enhanced security.
- Personalized user experience.

### Responsive Design
- Mobile-friendly and responsive interface.
- Clean and intuitive user experience.

---

## Technologies Used

### Backend
- Python
- Flask

### Frontend
- HTML5
- CSS3
- JavaScript

### Database
- SQLite

### AI Integration
- Google Gemini API

---

## Project Structure

```
HealthCare-4You/
│
├── static/
│   ├── style.css
│   ├── chatbot.js
│   ├── bmi.js
│   ├── login.js
│   └── signin.js
│
├── templates/
│
├── image/
│   ├── healthcare.png
│   ├── chatbot.png
│   └── stethoscope.png
│
├── appp.py
├── users.db
├── README.md
└── .env
```

---

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd HealthCare-4You
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file:

```env
GENAI_API_KEY=YOUR_API_KEY
```

### 4. Run the Application

```bash
python app.py
```

### 5. Open in Browser

```text
http://127.0.0.1:5000
```

---

## Project Objectives

- Provide quick access to basic healthcare information.
- Assist users with BMI calculation and health awareness.
- Demonstrate integration of Generative AI in healthcare applications.
- Practice full-stack web development using Flask.

---

## Future Enhancements

- Appointment Booking System
- Medical Report Analysis
- Health Tracking Dashboard
- Voice-Based Interaction
- Multi-Language Support

---
### Challenges Faced

One of the key challenges during development was integrating the Gemini GenAI API. Understanding API authentication, configuring requests, handling responses, and implementing effective prompts required additional learning and experimentation. Overcoming these challenges helped strengthen my understanding of AI API integration and backend development.

### Learning Experience

While developing this project, I faced challenges integrating the Gemini GenAI API. This experience helped me improve my understanding of API integration, prompt engineering, and handling AI-generated responses within a web application and I am still working on it.

## Author

**Yashika Jandaniya**

BCA Graduate | Aspiring Software Engineer | Python & AI Enthusiast

LinkedIn: www.linkedin.com/in/yashika-jandaniya-b58911282

---

If you found this project useful, consider giving it a star!

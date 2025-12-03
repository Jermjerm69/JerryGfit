# JerryGFit

JerryGFit is an AI-powered Progressive Web App (PWA) for fitness content creators.  
It combines AI caption/hashtag generation, task planning, risk tracking, and simple analytics in a single web-based dashboard.  
The platform was developed as a capstone project to explore how modern AI tools can support structured content planning and project management.

---

## Live Resources

- Live Application: https://jerrygfit.com  
- GitHub Repository: https://github.com/Jermjerm69/JerryGfit  
- API Documentation (Swagger): https://jerrygfit.com/api/v1/docs  
- Figma Design Prototype: https://www.figma.com/design/FrWFzkAw3go1dLny7QzZtJ/JerryGFit?node-id=0-1

---

## Features

- Google OAuth 2.0 login with JWT-based session handling
- AI Studio for generating captions, hashtags, and content ideas using GPT-4
- Task Planner for managing content-related tasks with status and deadlines
- Risk Register with probability/impact scoring and mitigation notes
- Simple analytics to visualize task activity and consistency over time
- Responsive PWA front-end for desktop and mobile browsers

---

## Technology Stack

- Frontend: Next.js (React, TypeScript), Tailwind CSS
- Backend: FastAPI (Python)
- Database: PostgreSQL
- AI: OpenAI GPT-4 API
- Auth: Google OAuth 2.0 + JWT
- Deployment: Docker, Nginx, DigitalOcean

---

## System Overview

The system follows a service-oriented architecture:

- Next.js/React frontend communicates with the FastAPI backend via JSON REST APIs.
- FastAPI exposes endpoints for authentication, tasks, risks, AI requests, and analytics.
- PostgreSQL stores users, projects, tasks, risks, and AI request logs.
- Nginx acts as a reverse proxy and terminates HTTPS, routing traffic to the appropriate service.

For more detailed diagrams (architecture, ERD, and UI screenshots), see the capstone product paper and associated documentation.

---

## Running the Project (Local Development)

This repository contains the code for both the frontend and backend.

1. Clone the repository:

```bash
git clone https://github.com/Jermjerm69/JerryGfit.git
cd JerryGfit


Backend (FastAPI):

Create and activate a Python virtual environment.

Install dependencies from requirements.txt.

Set environment variables (database URL, OpenAI API key, Google OAuth keys, JWT secret).

Run database migrations.

Start the API server with uvicorn.

Frontend (Next.js):

Move into the frontend directory.

Install dependencies with npm install or yarn.

Create .env.local and set NEXT_PUBLIC_API_URL to point to the backend.

Start the dev server with npm run dev or yarn dev.

For production, the application is containerized and deployed with Docker, Nginx, and PostgreSQL on a DigitalOcean droplet.


Project Context

JerryGFit was built as a capstone project for the
Bachelor of Science – School of Individualized Study.
The goal was to demonstrate:

Full-stack web development using modern frameworks

Integration of generative AI into a practical workflow

Application of project management concepts (risk register, burndown, phased development)

End-to-end deployment of a live PWA

License

This repository is provided for academic and portfolio purposes.



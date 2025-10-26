"""Database seed script with comprehensive demo data for JerryGFit."""
import sys
import json
from datetime import datetime, timedelta
from random import randint, choice

from app.database import SessionLocal
from app.models.user import User
from app.models.risk import Risk, RiskStatus, RiskSeverity
from app.models.task import Task, TaskStatus, TaskPriority
from app.models.engagement_metric import EngagementMetric
from app.models.ai_request import AIRequest
from app.core.security import get_password_hash


def seed_database():
    """Seed the database with demo data."""
    db = SessionLocal()

    try:
        # Check if data already exists
        if db.query(User).count() > 0:
            print("Database already contains data. Skipping seed...")
            return

        print("Seeding database...")

        # Create demo users
        demo_password = "demo123"
        demo_user = User(
            email="demo@jerrygfit.com",
            username="demo",
            full_name="Demo User",
            hashed_password=get_password_hash(demo_password[:72]),  # Bcrypt limit
            is_active=True,
            is_superuser=False,
        )
        db.add(demo_user)
        db.commit()
        db.refresh(demo_user)

        admin_password = "admin123"
        admin_user = User(
            email="admin@jerrygfit.com",
            username="admin",
            full_name="Admin User",
            hashed_password=get_password_hash(admin_password[:72]),  # Bcrypt limit
            is_active=True,
            is_superuser=True,
        )
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)

        print(f"Created users: {demo_user.username}, {admin_user.username}")

        # Create demo risks for demo user - Comprehensive set
        risks_data = [
            {
                "title": "Budget Overrun Risk",
                "description": "Project may exceed allocated budget due to scope creep and additional feature requests from stakeholders",
                "severity": RiskSeverity.HIGH,
                "status": RiskStatus.OPEN,
                "mitigation_plan": "Implement strict change control process and weekly budget reviews. All new features must go through approval workflow.",
            },
            {
                "title": "Resource Availability",
                "description": "Key team members may not be available full-time due to conflicting project priorities",
                "severity": RiskSeverity.MEDIUM,
                "status": RiskStatus.OPEN,
                "mitigation_plan": "Cross-train team members and identify backup resources. Maintain resource calendar with allocation percentages.",
            },
            {
                "title": "Technology Integration",
                "description": "Third-party API integration complexity underestimated, especially for payment gateway",
                "severity": RiskSeverity.HIGH,
                "status": RiskStatus.MITIGATED,
                "mitigation_plan": "Completed proof of concept, documented integration patterns. Created wrapper layer for easier maintenance.",
            },
            {
                "title": "User Adoption Risk",
                "description": "End users may resist adopting new platform due to learning curve and change fatigue",
                "severity": RiskSeverity.MEDIUM,
                "status": RiskStatus.OPEN,
                "mitigation_plan": "Develop comprehensive training program and user guides. Schedule demo sessions and create video tutorials.",
            },
            {
                "title": "Data Migration",
                "description": "Legacy data migration may encounter quality issues with inconsistent formats and missing fields",
                "severity": RiskSeverity.CRITICAL,
                "status": RiskStatus.OPEN,
                "mitigation_plan": "Perform data quality audit and implement validation scripts. Run pilot migration with 10% of data first.",
            },
            {
                "title": "Security Compliance",
                "description": "Application must meet GDPR and SOC 2 compliance requirements before launch",
                "severity": RiskSeverity.CRITICAL,
                "status": RiskStatus.OPEN,
                "mitigation_plan": "Engage security consultant for compliance audit. Implement data encryption and access controls.",
            },
            {
                "title": "Performance Bottlenecks",
                "description": "Database queries may not scale well with expected user load of 10,000+ concurrent users",
                "severity": RiskSeverity.HIGH,
                "status": RiskStatus.MITIGATED,
                "mitigation_plan": "Implemented database indexing, caching layer with Redis, and query optimization. Load testing completed.",
            },
            {
                "title": "Third-Party Dependency",
                "description": "Heavy reliance on OpenAI API for content generation - vendor lock-in concern",
                "severity": RiskSeverity.MEDIUM,
                "status": RiskStatus.OPEN,
                "mitigation_plan": "Design abstraction layer to support multiple AI providers. Evaluate alternatives like Anthropic Claude.",
            },
            {
                "title": "Mobile Responsiveness",
                "description": "Complex dashboard may not render well on mobile devices",
                "severity": RiskSeverity.LOW,
                "status": RiskStatus.MITIGATED,
                "mitigation_plan": "Implemented responsive design with Tailwind breakpoints. Tested on iOS and Android devices.",
            },
            {
                "title": "Testing Coverage Gap",
                "description": "Current test coverage is only 45%, target is 80% for production readiness",
                "severity": RiskSeverity.MEDIUM,
                "status": RiskStatus.OPEN,
                "mitigation_plan": "Allocate sprint capacity for test development. Focus on critical path and API endpoints first.",
            },
            {
                "title": "Deployment Pipeline",
                "description": "CI/CD pipeline not fully automated, manual steps prone to errors",
                "severity": RiskSeverity.MEDIUM,
                "status": RiskStatus.OPEN,
                "mitigation_plan": "Implement GitHub Actions for automated testing, building, and deployment. Add rollback mechanism.",
            },
            {
                "title": "API Rate Limiting",
                "description": "No rate limiting implemented, vulnerable to abuse and DDoS attacks",
                "severity": RiskSeverity.HIGH,
                "status": RiskStatus.OPEN,
                "mitigation_plan": "Implement rate limiting middleware with Redis. Set limits: 100 req/min for auth, 1000 req/min for API.",
            },
            {
                "title": "Documentation Debt",
                "description": "API documentation incomplete, making third-party integration difficult",
                "severity": RiskSeverity.LOW,
                "status": RiskStatus.OPEN,
                "mitigation_plan": "Use FastAPI's built-in Swagger docs. Add examples and description for all endpoints.",
            },
            {
                "title": "Timezone Handling",
                "description": "Application doesn't properly handle different timezones for global users",
                "severity": RiskSeverity.MEDIUM,
                "status": RiskStatus.MITIGATED,
                "mitigation_plan": "Store all timestamps in UTC. Convert to user's timezone on frontend. Added timezone selector in settings.",
            },
            {
                "title": "Content Moderation",
                "description": "User-generated content not being moderated, risk of inappropriate content",
                "severity": RiskSeverity.MEDIUM,
                "status": RiskStatus.OPEN,
                "mitigation_plan": "Implement content filtering API. Add reporting mechanism and admin moderation dashboard.",
            },
        ]

        for risk_data in risks_data:
            risk = Risk(**risk_data, owner_id=demo_user.id)
            db.add(risk)

        db.commit()
        print(f"Created {len(risks_data)} demo risks")

        # Create demo tasks for demo user - Comprehensive set across all statuses
        tasks_data = [
            # DONE Tasks (Completed)
            {
                "title": "Setup development environment",
                "description": "Install and configure all required development tools including Node.js, Python, PostgreSQL, and VS Code extensions",
                "status": TaskStatus.DONE,
                "priority": TaskPriority.HIGH,
                "completed": True,
                "due_date": datetime.utcnow() - timedelta(days=30),
            },
            {
                "title": "Design database schema",
                "description": "Create ERD and define all tables and relationships. Review with team and finalize structure.",
                "status": TaskStatus.DONE,
                "priority": TaskPriority.HIGH,
                "completed": True,
                "due_date": datetime.utcnow() - timedelta(days=28),
            },
            {
                "title": "Implement authentication system",
                "description": "Build JWT-based authentication with login/register endpoints. Include password hashing and token refresh.",
                "status": TaskStatus.DONE,
                "priority": TaskPriority.URGENT,
                "completed": True,
                "due_date": datetime.utcnow() - timedelta(days=25),
            },
            {
                "title": "Setup CI/CD pipeline",
                "description": "Configure GitHub Actions for automated testing and deployment to staging environment",
                "status": TaskStatus.DONE,
                "priority": TaskPriority.HIGH,
                "completed": True,
                "due_date": datetime.utcnow() - timedelta(days=22),
            },
            {
                "title": "Create project repository structure",
                "description": "Organize frontend and backend codebases with proper folder structure and configuration files",
                "status": TaskStatus.DONE,
                "priority": TaskPriority.MEDIUM,
                "completed": True,
                "due_date": datetime.utcnow() - timedelta(days=20),
            },
            {
                "title": "Install UI component library",
                "description": "Setup shadcn/ui with Tailwind CSS and configure theme system",
                "status": TaskStatus.DONE,
                "priority": TaskPriority.MEDIUM,
                "completed": True,
                "due_date": datetime.utcnow() - timedelta(days=18),
            },
            {
                "title": "Implement user model and migrations",
                "description": "Create User model with SQLAlchemy and run initial database migrations",
                "status": TaskStatus.DONE,
                "priority": TaskPriority.HIGH,
                "completed": True,
                "due_date": datetime.utcnow() - timedelta(days=15),
            },
            {
                "title": "Build authentication UI components",
                "description": "Create login and signup pages with form validation and error handling",
                "status": TaskStatus.DONE,
                "priority": TaskPriority.HIGH,
                "completed": True,
                "due_date": datetime.utcnow() - timedelta(days=12),
            },
            {
                "title": "Setup environment variables",
                "description": "Configure .env files for development, staging, and production environments",
                "status": TaskStatus.DONE,
                "priority": TaskPriority.HIGH,
                "completed": True,
                "due_date": datetime.utcnow() - timedelta(days=10),
            },
            {
                "title": "Create protected route wrapper",
                "description": "Implement ProtectedRoute component to guard authenticated pages",
                "status": TaskStatus.DONE,
                "priority": TaskPriority.HIGH,
                "completed": True,
                "due_date": datetime.utcnow() - timedelta(days=7),
            },

            # IN_PROGRESS Tasks (Currently working on)
            {
                "title": "Create API documentation",
                "description": "Document all API endpoints with examples using FastAPI's built-in Swagger documentation",
                "status": TaskStatus.IN_PROGRESS,
                "priority": TaskPriority.MEDIUM,
                "completed": False,
                "due_date": datetime.utcnow() + timedelta(days=2),
            },
            {
                "title": "Build risk management UI",
                "description": "Create React components for risk CRUD operations with filtering and sorting capabilities",
                "status": TaskStatus.IN_PROGRESS,
                "priority": TaskPriority.HIGH,
                "completed": False,
                "due_date": datetime.utcnow() + timedelta(days=3),
            },
            {
                "title": "Implement task board with drag-and-drop",
                "description": "Build Kanban board with drag-and-drop functionality using react-beautiful-dnd",
                "status": TaskStatus.IN_PROGRESS,
                "priority": TaskPriority.HIGH,
                "completed": False,
                "due_date": datetime.utcnow() + timedelta(days=4),
            },
            {
                "title": "Add real-time notifications",
                "description": "Implement WebSocket connection for real-time updates on tasks and risks",
                "status": TaskStatus.IN_PROGRESS,
                "priority": TaskPriority.MEDIUM,
                "completed": False,
                "due_date": datetime.utcnow() + timedelta(days=5),
            },
            {
                "title": "Optimize database queries",
                "description": "Add indexes and optimize N+1 queries. Implement query result caching with Redis.",
                "status": TaskStatus.IN_PROGRESS,
                "priority": TaskPriority.HIGH,
                "completed": False,
                "due_date": datetime.utcnow() + timedelta(days=6),
            },
            {
                "title": "Create engagement metrics dashboard",
                "description": "Build analytics dashboard showing user engagement, task completion rates, and risk trends",
                "status": TaskStatus.IN_PROGRESS,
                "priority": TaskPriority.MEDIUM,
                "completed": False,
                "due_date": datetime.utcnow() + timedelta(days=7),
            },

            # TODO Tasks (Planned)
            {
                "title": "Add analytics dashboard",
                "description": "Create charts and metrics for project analytics using recharts library",
                "status": TaskStatus.TODO,
                "priority": TaskPriority.MEDIUM,
                "completed": False,
                "due_date": datetime.utcnow() + timedelta(days=8),
            },
            {
                "title": "Integrate AI content generation",
                "description": "Connect OpenAI API for automated content suggestions, captions, and hashtags",
                "status": TaskStatus.TODO,
                "priority": TaskPriority.HIGH,
                "completed": False,
                "due_date": datetime.utcnow() + timedelta(days=10),
            },
            {
                "title": "Write unit tests for API endpoints",
                "description": "Achieve 80% code coverage with pytest. Focus on authentication and CRUD operations.",
                "status": TaskStatus.TODO,
                "priority": TaskPriority.MEDIUM,
                "completed": False,
                "due_date": datetime.utcnow() + timedelta(days=12),
            },
            {
                "title": "Implement user settings page",
                "description": "Build settings page for profile updates, password changes, and preferences",
                "status": TaskStatus.TODO,
                "priority": TaskPriority.LOW,
                "completed": False,
                "due_date": datetime.utcnow() + timedelta(days=14),
            },
            {
                "title": "Add file upload functionality",
                "description": "Implement file upload for user avatars and risk attachments using S3 or local storage",
                "status": TaskStatus.TODO,
                "priority": TaskPriority.MEDIUM,
                "completed": False,
                "due_date": datetime.utcnow() + timedelta(days=15),
            },
            {
                "title": "Deploy to staging environment",
                "description": "Set up staging environment on AWS/DigitalOcean and deploy application with proper monitoring",
                "status": TaskStatus.TODO,
                "priority": TaskPriority.HIGH,
                "completed": False,
                "due_date": datetime.utcnow() + timedelta(days=18),
            },
            {
                "title": "Implement search functionality",
                "description": "Add global search for tasks, risks, and users with autocomplete",
                "status": TaskStatus.TODO,
                "priority": TaskPriority.MEDIUM,
                "completed": False,
                "due_date": datetime.utcnow() + timedelta(days=20),
            },
            {
                "title": "Add email notifications",
                "description": "Setup email service (SendGrid/Mailgun) for task assignments and risk alerts",
                "status": TaskStatus.TODO,
                "priority": TaskPriority.LOW,
                "completed": False,
                "due_date": datetime.utcnow() + timedelta(days=22),
            },
            {
                "title": "Create mobile responsive layouts",
                "description": "Optimize all pages for mobile devices with proper breakpoints and touch interactions",
                "status": TaskStatus.TODO,
                "priority": TaskPriority.MEDIUM,
                "completed": False,
                "due_date": datetime.utcnow() + timedelta(days=24),
            },
            {
                "title": "Implement role-based access control",
                "description": "Add roles (admin, manager, user) with different permission levels",
                "status": TaskStatus.TODO,
                "priority": TaskPriority.HIGH,
                "completed": False,
                "due_date": datetime.utcnow() + timedelta(days=25),
            },
            {
                "title": "Add data export functionality",
                "description": "Allow users to export tasks and risks to CSV, PDF, and Excel formats",
                "status": TaskStatus.TODO,
                "priority": TaskPriority.LOW,
                "completed": False,
                "due_date": datetime.utcnow() + timedelta(days=28),
            },

            # BLOCKED Tasks
            {
                "title": "Integrate payment gateway",
                "description": "Setup Stripe integration for subscription payments. Blocked waiting for legal approval.",
                "status": TaskStatus.BLOCKED,
                "priority": TaskPriority.URGENT,
                "completed": False,
                "due_date": datetime.utcnow() + timedelta(days=9),
            },
            {
                "title": "Setup production database",
                "description": "Configure production PostgreSQL instance. Blocked by infrastructure team approval.",
                "status": TaskStatus.BLOCKED,
                "priority": TaskPriority.HIGH,
                "completed": False,
                "due_date": datetime.utcnow() + timedelta(days=16),
            },
            {
                "title": "Implement SSO integration",
                "description": "Add Google and Microsoft SSO login options. Blocked waiting for OAuth credentials.",
                "status": TaskStatus.BLOCKED,
                "priority": TaskPriority.MEDIUM,
                "completed": False,
                "due_date": datetime.utcnow() + timedelta(days=21),
            },
        ]

        for task_data in tasks_data:
            task = Task(**task_data, owner_id=demo_user.id)
            db.add(task)

        db.commit()
        print(f"Created {len(tasks_data)} demo tasks")

        # Create engagement metrics - Comprehensive tracking over time
        metrics_data = [
            # Login activity over the past 30 days
            {"metric_type": "login", "metric_value": 1, "metric_metadata": json.dumps({"source": "web", "device": "desktop"})},
            {"metric_type": "login", "metric_value": 1, "metric_metadata": json.dumps({"source": "web", "device": "mobile"})},
            {"metric_type": "login", "metric_value": 1, "metric_metadata": json.dumps({"source": "web", "device": "desktop"})},

            # Task completion activity
            {"metric_type": "tasks_completed", "metric_value": 10, "metric_metadata": json.dumps({"period": "last_30_days", "completion_rate": 0.33})},
            {"metric_type": "tasks_created", "metric_value": 30, "metric_metadata": json.dumps({"period": "last_30_days"})},
            {"metric_type": "tasks_updated", "metric_value": 15, "metric_metadata": json.dumps({"period": "last_7_days"})},

            # Risk management activity
            {"metric_type": "risks_created", "metric_value": 15, "metric_metadata": json.dumps({"period": "last_30_days"})},
            {"metric_type": "risks_mitigated", "metric_value": 4, "metric_metadata": json.dumps({"critical": 1, "high": 2, "medium": 1})},
            {"metric_type": "risks_updated", "metric_value": 8, "metric_metadata": json.dumps({"period": "last_7_days"})},

            # AI usage patterns
            {"metric_type": "ai_usage", "metric_value": 5, "metric_metadata": json.dumps({"type": "caption_generation", "success_rate": 1.0})},
            {"metric_type": "ai_usage", "metric_value": 3, "metric_metadata": json.dumps({"type": "hashtag_generation", "success_rate": 1.0})},
            {"metric_type": "ai_usage", "metric_value": 2, "metric_metadata": json.dumps({"type": "content_summary", "success_rate": 1.0})},

            # Session and engagement metrics
            {"metric_type": "session_duration", "metric_value": 45.5, "metric_metadata": json.dumps({"date": "2025-01-25", "pages_visited": 8})},
            {"metric_type": "session_duration", "metric_value": 62.3, "metric_metadata": json.dumps({"date": "2025-01-24", "pages_visited": 12})},
            {"metric_type": "session_duration", "metric_value": 38.7, "metric_metadata": json.dumps({"date": "2025-01-23", "pages_visited": 6})},

            # Dashboard interactions
            {"metric_type": "dashboard_view", "metric_value": 25, "metric_metadata": json.dumps({"period": "last_30_days", "avg_time": 120})},
            {"metric_type": "analytics_view", "metric_value": 12, "metric_metadata": json.dumps({"period": "last_30_days", "charts_viewed": ["burndown", "velocity", "risks"]})},

            # Feature usage
            {"metric_type": "feature_usage", "metric_value": 18, "metric_metadata": json.dumps({"feature": "kanban_board", "interactions": 45})},
            {"metric_type": "feature_usage", "metric_value": 22, "metric_metadata": json.dumps({"feature": "risk_register", "interactions": 67})},
            {"metric_type": "feature_usage", "metric_value": 8, "metric_metadata": json.dumps({"feature": "ai_studio", "interactions": 10})},
        ]

        for metric_data in metrics_data:
            metric = EngagementMetric(**metric_data, user_id=demo_user.id)
            db.add(metric)

        db.commit()
        print(f"Created {len(metrics_data)} engagement metrics")

        # Create AI request history - Showcase AI content generation features
        ai_requests_data = [
            {
                "request_type": "caption",
                "prompt": "Generate an inspiring fitness caption for a morning workout photo",
                "response": {
                    "content": "Rise and grind! 💪 There's no better time than NOW to invest in yourself. Every drop of sweat is a step closer to your goals. Remember: The only bad workout is the one that didn't happen. Let's make today count!",
                    "model": "gpt-4",
                    "timestamp": datetime.utcnow().isoformat()
                },
                "tokens_used": 156,
            },
            {
                "request_type": "hashtag",
                "prompt": "Create trending hashtags for a fitness transformation post",
                "response": {
                    "content": "#FitnessJourney #TransformationTuesday #FitLife #HealthyLifestyle #GymMotivation #FitnessGoals #WorkoutRoutine #BodyTransformation #FitFam #NoPainNoGain #GymLife #FitnessAddict #GetFit #HealthyLiving #FitnessInspiration",
                    "model": "gpt-4",
                    "timestamp": datetime.utcnow().isoformat()
                },
                "tokens_used": 98,
            },
            {
                "request_type": "summary",
                "prompt": "Summarize this workout plan: Full body strength training with focus on compound movements",
                "response": {
                    "content": "This comprehensive full-body strength program emphasizes compound exercises like squats, deadlifts, bench press, and overhead press. Designed to build overall muscle mass and strength through multi-joint movements that engage multiple muscle groups simultaneously. Ideal for efficient muscle building and fat loss.",
                    "model": "gpt-4",
                    "timestamp": datetime.utcnow().isoformat()
                },
                "tokens_used": 134,
            },
            {
                "request_type": "caption",
                "prompt": "Write a motivational caption about leg day",
                "response": {
                    "content": "Leg day: the foundation of champions! 🦵 While everyone else is skipping leg day, you're building the powerhouse that carries you through life. Strong legs = strong foundation. Your future self will thank you for not skipping today! #LegDayBestDay",
                    "model": "gpt-4",
                    "timestamp": (datetime.utcnow() - timedelta(days=2)).isoformat()
                },
                "tokens_used": 142,
            },
            {
                "request_type": "hashtag",
                "prompt": "Generate hashtags for a nutrition and meal prep post",
                "response": {
                    "content": "#MealPrep #HealthyEating #NutritionTips #CleanEating #FitFood #MealPrepSunday #HealthyRecipes #FitnessNutrition #BalancedDiet #FoodPrep #NutritionCoach #EatClean #HealthyMeals #MacroTracking #FuelYourBody",
                    "model": "gpt-4",
                    "timestamp": (datetime.utcnow() - timedelta(days=3)).isoformat()
                },
                "tokens_used": 89,
            },
            {
                "request_type": "caption",
                "prompt": "Create an engaging caption for a yoga and flexibility post",
                "response": {
                    "content": "Find your balance, find your peace. 🧘‍♀️ Yoga isn't about touching your toes, it's about what you learn on the way down. Flexibility of body leads to flexibility of mind. Take a deep breath and let go of everything that doesn't serve you. Namaste! ✨",
                    "model": "gpt-4",
                    "timestamp": (datetime.utcnow() - timedelta(days=5)).isoformat()
                },
                "tokens_used": 148,
            },
            {
                "request_type": "summary",
                "prompt": "Summarize benefits of high-intensity interval training",
                "response": {
                    "content": "HIIT (High-Intensity Interval Training) offers time-efficient fat burning, increased metabolism that lasts hours post-workout, improved cardiovascular health, and preservation of muscle mass while cutting fat. Alternating intense bursts with recovery periods maximizes calorie burn in minimal time.",
                    "model": "gpt-4",
                    "timestamp": (datetime.utcnow() - timedelta(days=7)).isoformat()
                },
                "tokens_used": 128,
            },
            {
                "request_type": "caption",
                "prompt": "Write a caption about consistency and progress",
                "response": {
                    "content": "Progress isn't always linear, but it's always worth it. 📈 Some days you'll feel unstoppable, other days you'll struggle through warm-ups. That's okay! What matters is showing up consistently. Trust the process, celebrate small wins, and remember: you're lapping everyone on the couch. Keep pushing! 💯",
                    "model": "gpt-4",
                    "timestamp": (datetime.utcnow() - timedelta(days=10)).isoformat()
                },
                "tokens_used": 164,
            },
            {
                "request_type": "hashtag",
                "prompt": "Create hashtags for a personal training service promotion",
                "response": {
                    "content": "#PersonalTrainer #FitnessCoach #OnlineCoaching #PersonalTraining #FitnessTrainer #PTLife #GetFitWithMe #TrainWithMe #FitnessCoaching #WorkoutPlan #CustomWorkout #FitnessExpert #TransformationCoach #OnlinePersonalTrainer #FitnessGuide",
                    "model": "gpt-4",
                    "timestamp": (datetime.utcnow() - timedelta(days=12)).isoformat()
                },
                "tokens_used": 92,
            },
            {
                "request_type": "summary",
                "prompt": "Explain the importance of rest and recovery in fitness",
                "response": {
                    "content": "Rest and recovery are crucial for muscle growth, injury prevention, and performance optimization. During rest, muscles repair and strengthen, nervous system recovers, and hormones rebalance. Adequate sleep, active recovery, and scheduled rest days prevent overtraining and ensure sustainable progress.",
                    "model": "gpt-4",
                    "timestamp": (datetime.utcnow() - timedelta(days=15)).isoformat()
                },
                "tokens_used": 119,
            },
        ]

        for ai_request_data in ai_requests_data:
            ai_request = AIRequest(**ai_request_data, user_id=demo_user.id)
            db.add(ai_request)

        db.commit()
        print(f"Created {len(ai_requests_data)} AI request records")

        print("\n✅ Database seeded successfully!")
        print("\nDemo credentials:")
        print("  Username: demo")
        print("  Password: demo123")
        print("\nAdmin credentials:")
        print("  Username: admin")
        print("  Password: admin123")
        print(f"\n📊 Summary:")
        print(f"  - {len(risks_data)} risks created")
        print(f"  - {len(tasks_data)} tasks created (10 DONE, 6 IN_PROGRESS, 11 TODO, 3 BLOCKED)")
        print(f"  - {len(metrics_data)} engagement metrics")
        print(f"  - {len(ai_requests_data)} AI generations")

    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        db.rollback()
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()

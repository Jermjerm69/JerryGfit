"""
Seed script for CreatorsApp - Fitness Coaching Platform
Generates realistic data for all models to demonstrate the platform capabilities
"""

import sys
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.database import SessionLocal, engine
from app.models.user import User, UserRole
from app.models.project import Project
from app.models.task import Task
from app.models.risk import Risk, RiskStatus, RiskSeverity, RiskProbability, RiskImpact
from app.models.post import Post
from app.models.ai_request import AIRequest
from app.models.engagement_metric import EngagementMetric
from app.core.security import get_password_hash


def clear_all_data(db: Session):
    """Clear all existing data (use with caution!)"""
    print("⚠️  Clearing all existing data...")
    db.query(AIRequest).delete()
    db.query(Post).delete()
    db.query(Risk).delete()
    db.query(Task).delete()
    db.query(Project).delete()
    db.query(EngagementMetric).delete()  # Delete engagement metrics before users
    db.query(User).delete()
    db.commit()
    print("✓ All data cleared\n")


def seed_users(db: Session) -> dict:
    """Seed users with different roles"""
    print("👥 Seeding users...")

    users = [
        User(
            email="admin@creatorsapp.com",
            username="admin",
            full_name="Admin User",
            hashed_password=get_password_hash("Admin123!"),
            role=UserRole.ADMIN,
            is_superuser=True,
            notification_preferences={
                "email_notifications": True,
                "push_notifications": True,
                "task_reminders": True,
                "weekly_reports": True,
                "risk_alerts": True
            },
            user_preferences={
                "language": "english",
                "date_format": "MM/DD/YYYY",
                "time_format": "12-hour"
            }
        ),
        User(
            email="coach@fitness.com",
            username="fitnesscoach",
            full_name="Sarah Johnson",
            hashed_password=get_password_hash("Coach123!"),
            role=UserRole.COACH,
            notification_preferences={
                "email_notifications": True,
                "push_notifications": True,
                "task_reminders": True,
                "weekly_reports": True,
                "risk_alerts": True
            },
            user_preferences={
                "language": "english",
                "date_format": "MM/DD/YYYY",
                "time_format": "24-hour"
            }
        ),
        User(
            email="creator@youtube.com",
            username="jerrygfit",
            full_name="Jerry Garcia",
            hashed_password=get_password_hash("Creator123!"),
            role=UserRole.CREATOR,
            notification_preferences={
                "email_notifications": True,
                "push_notifications": True,
                "task_reminders": True,
                "weekly_reports": False,
                "risk_alerts": True
            },
            user_preferences={
                "language": "english",
                "date_format": "DD/MM/YYYY",
                "time_format": "12-hour"
            }
        ),
        User(
            email="user@example.com",
            username="gymuser",
            full_name="Mike Thompson",
            hashed_password=get_password_hash("User123!"),
            role=UserRole.USER,
            notification_preferences={
                "email_notifications": True,
                "push_notifications": False,
                "task_reminders": True,
                "weekly_reports": False,
                "risk_alerts": False
            },
            user_preferences={
                "language": "english",
                "date_format": "MM/DD/YYYY",
                "time_format": "12-hour"
            }
        ),
    ]

    for user in users:
        db.add(user)

    db.commit()

    # Refresh to get IDs
    for user in users:
        db.refresh(user)

    user_dict = {user.username: user for user in users}

    print(f"✓ Created {len(users)} users")
    for user in users:
        print(f"  - {user.full_name} ({user.username}) - {user.role}")
    print()

    return user_dict


def seed_projects(db: Session, users: dict) -> list:
    """Seed projects for coaches and creators"""
    print("📁 Seeding projects...")

    coach = users["fitnesscoach"]
    creator = users["jerrygfit"]

    projects_data = [
        # Coach's Projects
        {
            "name": "Summer Fitness Program 2025",
            "description": "12-week transformation program for summer body goals. Includes workout plans, nutrition guides, and weekly check-ins.",
            "status": "active",
            "progress": 45,
            "due_date": datetime.now() + timedelta(days=60),
            "owner_id": coach.id
        },
        {
            "name": "Corporate Wellness Initiative",
            "description": "6-month wellness program for TechCorp employees. Focus on desk exercises, stress management, and healthy habits.",
            "status": "active",
            "progress": 70,
            "due_date": datetime.now() + timedelta(days=120),
            "owner_id": coach.id
        },
        {
            "name": "Online Coaching Platform Launch",
            "description": "Launch new online coaching platform with video courses and live sessions.",
            "status": "on_hold",
            "progress": 30,
            "due_date": datetime.now() + timedelta(days=90),
            "owner_id": coach.id
        },

        # Creator's Projects
        {
            "name": "YouTube Content Calendar Q2",
            "description": "Plan and create 30 fitness videos for YouTube: 15 workout tutorials, 10 nutrition tips, 5 transformation stories.",
            "status": "active",
            "progress": 60,
            "due_date": datetime.now() + timedelta(days=45),
            "owner_id": creator.id
        },
        {
            "name": "Instagram Reels - Home Workout Series",
            "description": "20-part series of 30-second home workout reels targeting abs, arms, legs, and full body.",
            "status": "active",
            "progress": 80,
            "due_date": datetime.now() + timedelta(days=15),
            "owner_id": creator.id
        },
        {
            "name": "Fitness App Collaboration",
            "description": "Partner with FitTech app to create exclusive workout content and training programs.",
            "status": "active",
            "progress": 25,
            "due_date": datetime.now() + timedelta(days=75),
            "owner_id": creator.id
        },
        {
            "name": "E-book: 30 Days to Stronger Core",
            "description": "Write and design comprehensive e-book with daily core exercises, nutrition tips, and progress trackers.",
            "status": "completed",
            "progress": 100,
            "due_date": datetime.now() - timedelta(days=10),
            "owner_id": creator.id
        },
    ]

    projects = []
    for proj_data in projects_data:
        project = Project(**proj_data)
        db.add(project)
        projects.append(project)

    db.commit()

    for project in projects:
        db.refresh(project)

    print(f"✓ Created {len(projects)} projects")
    for project in projects:
        print(f"  - {project.name} ({project.status}, {project.progress}%)")
    print()

    return projects


def seed_tasks(db: Session, projects: list) -> list:
    """Seed tasks for each project"""
    print("✅ Seeding tasks...")

    tasks_data = []

    # Summer Fitness Program tasks
    summer_project = [p for p in projects if "Summer Fitness" in p.name][0]
    tasks_data.extend([
        {
            "title": "Design 12-week workout plan",
            "description": "Create progressive overload plan with 4 training phases: Foundation, Build, Peak, Maintenance",
            "status": "done",
            "priority": "high",
            "completed": True,
            "due_date": datetime.now() - timedelta(days=30),
            "owner_id": summer_project.owner_id
        },
        {
            "title": "Create nutrition guide PDF",
            "description": "Macro calculations, meal prep ideas, grocery lists, and recipe suggestions",
            "status": "done",
            "priority": "high",
            "completed": True,
            "due_date": datetime.now() - timedelta(days=20),
            "owner_id": summer_project.owner_id
        },
        {
            "title": "Record exercise demonstration videos",
            "description": "Film proper form for 50 key exercises with common mistakes highlighted",
            "status": "in_progress",
            "priority": "high",
            "completed": False,
            "due_date": datetime.now() + timedelta(days=10),
            "owner_id": summer_project.owner_id
        },
        {
            "title": "Set up client progress tracking system",
            "description": "Create spreadsheet template for weekly measurements and progress photos",
            "status": "todo",
            "priority": "medium",
            "completed": False,
            "due_date": datetime.now() + timedelta(days=15),
            "owner_id": summer_project.owner_id
        },
        {
            "title": "Launch program marketing campaign",
            "description": "Social media posts, email sequence, early bird discount promotion",
            "status": "todo",
            "priority": "high",
            "completed": False,
            "due_date": datetime.now() + timedelta(days=25),
            "owner_id": summer_project.owner_id
        },
    ])

    # Corporate Wellness tasks
    corporate_project = [p for p in projects if "Corporate Wellness" in p.name][0]
    tasks_data.extend([
        {
            "title": "Conduct employee fitness assessment",
            "description": "Survey 150 employees about current fitness levels and goals",
            "status": "done",
            "priority": "high",
            "completed": True,
            "due_date": datetime.now() - timedelta(days=90),
            "owner_id": corporate_project.owner_id
        },
        {
            "title": "Design desk exercise program",
            "description": "15-minute routines for office workers: stretching, posture fixes, energy boosters",
            "status": "done",
            "priority": "high",
            "completed": True,
            "due_date": datetime.now() - timedelta(days=60),
            "owner_id": corporate_project.owner_id
        },
        {
            "title": "Host weekly group fitness sessions",
            "description": "Tuesday/Thursday lunchtime sessions: yoga, HIIT, strength training rotation",
            "status": "in_progress",
            "priority": "medium",
            "completed": False,
            "due_date": datetime.now() + timedelta(days=30),
            "owner_id": corporate_project.owner_id
        },
        {
            "title": "Create wellness challenge competition",
            "description": "30-day step challenge with prizes and team leaderboards",
            "status": "in_progress",
            "priority": "medium",
            "completed": False,
            "due_date": datetime.now() + timedelta(days=20),
            "owner_id": corporate_project.owner_id
        },
    ])

    # YouTube Content Calendar tasks
    youtube_project = [p for p in projects if "YouTube Content" in p.name][0]
    tasks_data.extend([
        {
            "title": "Film 'Perfect Push-Up Form' tutorial",
            "description": "10-minute video covering variations: standard, wide, diamond, decline",
            "status": "done",
            "priority": "high",
            "completed": True,
            "due_date": datetime.now() - timedelta(days=5),
            "owner_id": youtube_project.owner_id
        },
        {
            "title": "Edit and upload deadlift tutorial",
            "description": "Full editing with slow-mo form checks, add B-roll gym footage",
            "status": "in_progress",
            "priority": "urgent",
            "completed": False,
            "due_date": datetime.now() + timedelta(days=2),
            "owner_id": youtube_project.owner_id
        },
        {
            "title": "Script 'Top 10 Protein Sources' video",
            "description": "Research, write script, create graphics for each protein source",
            "status": "in_progress",
            "priority": "high",
            "completed": False,
            "due_date": datetime.now() + timedelta(days=7),
            "owner_id": youtube_project.owner_id
        },
        {
            "title": "Record client transformation interview",
            "description": "Film before/after story with John (50lb weight loss journey)",
            "status": "todo",
            "priority": "medium",
            "completed": False,
            "due_date": datetime.now() + timedelta(days=12),
            "owner_id": youtube_project.owner_id
        },
        {
            "title": "Create YouTube thumbnails batch",
            "description": "Design 10 eye-catching thumbnails for upcoming videos",
            "status": "blocked",
            "priority": "medium",
            "completed": False,
            "due_date": datetime.now() + timedelta(days=5),
            "owner_id": youtube_project.owner_id
        },
    ])

    # Instagram Reels tasks
    reels_project = [p for p in projects if "Instagram Reels" in p.name][0]
    tasks_data.extend([
        {
            "title": "Film 5 ab exercise reels",
            "description": "Crunches, planks, Russian twists, mountain climbers, bicycle crunches",
            "status": "done",
            "priority": "high",
            "completed": True,
            "due_date": datetime.now() - timedelta(days=8),
            "owner_id": reels_project.owner_id
        },
        {
            "title": "Edit and post arm workout reels",
            "description": "Bicep curls, tricep dips, shoulder press - add trending audio",
            "status": "in_progress",
            "priority": "high",
            "completed": False,
            "due_date": datetime.now() + timedelta(days=3),
            "owner_id": reels_project.owner_id
        },
        {
            "title": "Create leg day reel series",
            "description": "Squats, lunges, deadlifts, calf raises - 4 reels total",
            "status": "todo",
            "priority": "medium",
            "completed": False,
            "due_date": datetime.now() + timedelta(days=10),
            "owner_id": reels_project.owner_id
        },
    ])

    # Fitness App Collaboration tasks
    app_project = [p for p in projects if "Fitness App" in p.name][0]
    tasks_data.extend([
        {
            "title": "Review partnership contract",
            "description": "Legal review of exclusivity clause and payment terms",
            "status": "in_progress",
            "priority": "urgent",
            "completed": False,
            "due_date": datetime.now() + timedelta(days=5),
            "owner_id": app_project.owner_id
        },
        {
            "title": "Record 10 exclusive workout videos",
            "description": "Full-body, upper, lower, core, cardio routines for app users",
            "status": "todo",
            "priority": "high",
            "completed": False,
            "due_date": datetime.now() + timedelta(days=30),
            "owner_id": app_project.owner_id
        },
    ])

    tasks = []
    for task_data in tasks_data:
        task = Task(**task_data)
        db.add(task)
        tasks.append(task)

    db.commit()

    for task in tasks:
        db.refresh(task)

    print(f"✓ Created {len(tasks)} tasks")
    statuses = {}
    for task in tasks:
        statuses[task.status] = statuses.get(task.status, 0) + 1
    for status, count in statuses.items():
        print(f"  - {status}: {count}")
    print()

    return tasks


def seed_risks(db: Session, projects: list) -> list:
    """Seed risks for projects"""
    print("⚠️  Seeding risks...")

    risks_data = []

    # Summer Fitness Program risks
    summer_project = [p for p in projects if "Summer Fitness" in p.name][0]
    risks_data.extend([
        {
            "title": "Low client enrollment",
            "description": "Only 15 signups so far, need 50 to break even on program costs",
            "severity": "high",
            "probability": "medium",
            "impact": "high",
            "status": "open",
            "mitigation_plan": "Launch early bird discount (20% off), increase social media ads budget by $500, reach out to past clients with personalized emails",
            "owner_id": summer_project.owner_id
        },
        {
            "title": "Video equipment malfunction",
            "description": "Camera has been glitching during recordings, might need replacement",
            "severity": "medium",
            "probability": "high",
            "impact": "medium",
            "status": "open",
            "mitigation_plan": "Order backup camera ($800 budget approved), rent equipment if needed, have phone as emergency backup",
            "owner_id": summer_project.owner_id
        },
        {
            "title": "Nutrition guide copyright issues",
            "description": "Some recipe sources need proper attribution to avoid copyright claims",
            "severity": "low",
            "probability": "low",
            "impact": "medium",
            "status": "mitigated",
            "mitigation_plan": "Hired lawyer to review all content, rewrote 5 recipes to be original, added proper citations for inspiration sources",
            "owner_id": summer_project.owner_id
        },
    ])

    # Corporate Wellness risks
    corporate_project = [p for p in projects if "Corporate Wellness" in p.name][0]
    risks_data.extend([
        {
            "title": "Low employee participation rate",
            "description": "Only 30% of employees attending fitness sessions, target was 60%",
            "severity": "medium",
            "probability": "high",
            "impact": "medium",
            "status": "open",
            "mitigation_plan": "Survey non-participants for feedback, offer multiple session times, create incentive program (raffle prizes for attendees)",
            "owner_id": corporate_project.owner_id
        },
        {
            "title": "Contract renewal uncertainty",
            "description": "Company budget cuts might affect program renewal in Q4",
            "severity": "critical",
            "probability": "medium",
            "impact": "critical",
            "status": "open",
            "mitigation_plan": "Prepare ROI report showing productivity gains and reduced sick days, meet with HR director monthly, offer discounted renewal rate",
            "owner_id": corporate_project.owner_id
        },
    ])

    # YouTube Content risks
    youtube_project = [p for p in projects if "YouTube Content" in p.name][0]
    risks_data.extend([
        {
            "title": "Deadline crunch for Q2 content",
            "description": "Behind schedule by 5 videos, might miss upload consistency goals",
            "severity": "high",
            "probability": "high",
            "impact": "high",
            "status": "open",
            "mitigation_plan": "Hire video editor ($400/video), batch film 8 videos this weekend, repurpose old content with updates",
            "owner_id": youtube_project.owner_id
        },
        {
            "title": "Copyright strike on background music",
            "description": "Recent video flagged for music copyright, 2 more strikes = channel penalty",
            "severity": "critical",
            "probability": "low",
            "impact": "critical",
            "status": "mitigated",
            "mitigation_plan": "Subscribed to Epidemic Sound ($30/month), removed flagged video, reviewed all past videos for copyright issues",
            "owner_id": youtube_project.owner_id
        },
        {
            "title": "Thumbnail designer unavailable",
            "description": "Regular designer on vacation for 3 weeks, thumbnails are key to views",
            "severity": "medium",
            "probability": "high",
            "impact": "medium",
            "status": "closed",
            "mitigation_plan": "Found backup designer on Fiverr, learned Canva basics to DIY if needed, designer created templates for easy edits",
            "owner_id": youtube_project.owner_id
        },
    ])

    # Fitness App risks
    app_project = [p for p in projects if "Fitness App" in p.name][0]
    risks_data.extend([
        {
            "title": "Exclusivity clause conflict",
            "description": "Contract prevents posting similar content on YouTube for 6 months",
            "severity": "high",
            "probability": "high",
            "impact": "high",
            "status": "open",
            "mitigation_plan": "Negotiating clause modification with app legal team, may need to pivot content strategy, considering alternative revenue streams",
            "owner_id": app_project.owner_id
        },
        {
            "title": "App platform technical issues",
            "description": "Beta version has frequent crashes, might delay launch",
            "severity": "medium",
            "probability": "medium",
            "impact": "medium",
            "status": "open",
            "mitigation_plan": "Weekly sync with dev team, agreed on bug fix timeline, backup plan to launch with fewer videos initially",
            "owner_id": app_project.owner_id
        },
    ])

    risks = []
    for risk_data in risks_data:
        # Create Risk object directly with string values (SQLAlchemy will handle conversion)
        risk = Risk(**risk_data)
        db.add(risk)
        risks.append(risk)

    db.commit()

    for risk in risks:
        db.refresh(risk)

    print(f"✓ Created {len(risks)} risks")
    severities = {}
    for risk in risks:
        severities[risk.severity] = severities.get(risk.severity, 0) + 1
    for severity, count in severities.items():
        print(f"  - {severity}: {count}")
    print()

    return risks


def seed_posts(db: Session, users: dict, projects: list) -> list:
    """Seed social media posts"""
    print("📱 Seeding posts...")

    creator = users["jerrygfit"]
    youtube_project = [p for p in projects if "YouTube Content" in p.name][0]
    reels_project = [p for p in projects if "Instagram Reels" in p.name][0]

    posts_data = [
        {
            "title": "Perfect Push-Up Tutorial",
            "content": "Step-by-step guide to mastering push-ups with 4 variations for all fitness levels!",
            "caption": "💪 PERFECT YOUR PUSH-UP FORM! 💪\n\nMaster the king of bodyweight exercises with these 4 variations:\n\n1️⃣ Standard Push-Up - Build chest & triceps\n2️⃣ Wide Grip - Target outer chest\n3️⃣ Diamond - Hit those triceps hard\n4️⃣ Decline - Upper chest activation\n\n✅ Keep core tight\n✅ Elbows at 45°\n✅ Full range of motion\n\nWhich variation is your favorite? Drop a 💪 below!\n\n🎥 Full tutorial link in bio\n\n#PushUpChallenge #FitnessMotivation #WorkoutTips",
            "hashtags": "#fitness #workout #gym #pushups #bodyweight #fitnessmotivation #gymtips #training #exercise #fitnessjourney",
            "likes": 1847,
            "comments": 93,
            "shares": 124,
            "engagement_rate": 11.2,
            "project_id": youtube_project.id,
            "user_id": creator.id,
            "published_at": datetime.now() - timedelta(days=5)
        },
        {
            "title": "30-Second Ab Burner",
            "content": "Quick and effective ab routine you can do anywhere, no equipment needed!",
            "caption": "🔥 30-SECOND AB BURNER 🔥\n\nNo equipment? No problem!\n\nTry this quick core crusher:\n• Mountain Climbers x 30 sec\n• Rest 10 sec\n• Repeat 3 times\n\nYour abs will be SCREAMING! 😤\n\nSave this for your next workout! 💾\n\n#absworkout #coreworkout #homeworkout #fitnessreels",
            "hashtags": "#abs #core #homeworkout #quickworkout #fitness #gym #workout #exercise #fitnessreels #trending",
            "likes": 3241,
            "comments": 156,
            "shares": 418,
            "engagement_rate": 14.8,
            "project_id": reels_project.id,
            "user_id": creator.id,
            "published_at": datetime.now() - timedelta(days=3)
        },
        {
            "title": "Top 5 Protein Sources",
            "content": "Complete guide to the best protein sources for muscle building and recovery",
            "caption": "🥩 TOP 5 PROTEIN SOURCES FOR GAINS 🥩\n\n1. Chicken Breast - 31g per 100g\n2. Greek Yogurt - 10g per 100g\n3. Salmon - 25g per 100g\n4. Eggs - 13g per 100g\n5. Lentils - 9g per 100g (vegan!)\n\nWhich is YOUR go-to? Comment below! 👇\n\n💡 Pro tip: Combine sources throughout the day for optimal protein synthesis!\n\n🔗 Full nutrition breakdown in new video - link in bio\n\n#protein #nutrition #musclegain #fitness #healthy",
            "hashtags": "#protein #nutrition #healthyfood #fitness #muscle #bodybuilding #mealprep #fitnesstips #gains #gym",
            "likes": 2156,
            "comments": 187,
            "shares": 241,
            "engagement_rate": 12.5,
            "project_id": youtube_project.id,
            "user_id": creator.id,
            "published_at": datetime.now() - timedelta(days=8)
        },
        {
            "title": "Squat Form Check",
            "content": "Common squat mistakes and how to fix them for safer, more effective leg training",
            "caption": "⚠️ STOP! Are you making these SQUAT MISTAKES? ⚠️\n\n❌ Knees caving in\n❌ Rising on toes\n❌ Rounding lower back\n\n✅ DO THIS INSTEAD:\n✅ Knees track over toes\n✅ Weight on mid-foot\n✅ Chest proud, core tight\n\nTag someone who needs to see this! 👊\n\n#squats #legday #formcheck #fitnesstips",
            "hashtags": "#squat #legday #fitness #gym #workout #formcheck #fitnesstips #training #exercise #strength",
            "likes": 4128,
            "comments": 203,
            "shares": 567,
            "engagement_rate": 16.3,
            "project_id": reels_project.id,
            "user_id": creator.id,
            "published_at": datetime.now() - timedelta(days=1)
        },
        {
            "title": "Client Transformation: John's Journey",
            "content": "Incredible 50lb weight loss transformation story with John - dedication pays off!",
            "caption": "😭 THIS IS WHY I DO WHAT I DO 😭\n\nMeet John: Lost 50 lbs in 6 months!\n\n📉 300 lbs → 250 lbs\n📈 Can now play with his kids without getting tired\n💪 Went from 0 to 20 push-ups\n\n\"I thought it was impossible. Jerry showed me it wasn't.\" - John\n\nYour transformation starts TODAY. Link in bio to get started!\n\n#transformation #weightloss #success #motivation",
            "hashtags": "#transformation #weightloss #beforeandafter #fitness #motivation #success #fitnessmotivation #inspiration #results #coaching",
            "likes": 8934,
            "comments": 412,
            "shares": 1247,
            "engagement_rate": 22.7,
            "project_id": youtube_project.id,
            "user_id": creator.id,
            "published_at": datetime.now() - timedelta(days=12)
        },
    ]

    posts = []
    for post_data in posts_data:
        post = Post(**post_data)
        db.add(post)
        posts.append(post)

    db.commit()

    for post in posts:
        db.refresh(post)

    print(f"✓ Created {len(posts)} posts")
    total_engagement = sum(p.likes + p.comments + p.shares for p in posts)
    print(f"  - Total engagement: {total_engagement:,}")
    print(f"  - Avg engagement rate: {sum(p.engagement_rate for p in posts) / len(posts):.1f}%")
    print()

    return posts


def seed_ai_requests(db: Session, users: dict) -> list:
    """Seed AI Studio requests and responses"""
    print("🤖 Seeding AI requests...")

    creator = users["jerrygfit"]
    coach = users["fitnesscoach"]

    ai_requests_data = [
        {
            "user_id": creator.id,
            "request_type": "caption_generation",
            "prompt": "Create an engaging Instagram caption for a leg day workout video showing squats, lunges, and deadlifts",
            "response": {
                "caption": "🔥 LEG DAY = BEST DAY 🔥\n\nHit these 3 exercises for MASSIVE leg gains:\n\n1️⃣ Squats - King of leg exercises\n2️⃣ Lunges - Balance + strength\n3️⃣ Deadlifts - Posterior chain power\n\n💪 3 sets x 10-12 reps\n💪 Rest 90 seconds between sets\n💪 Focus on form over weight!\n\nWho's training legs today? Drop a 🦵 below!\n\n#LegDay #SquatGoals #FitnessMotivation #GymLife",
                "hashtags": ["LegDay", "SquatGoals", "FitnessMotivation", "GymLife", "Workout", "Fitness", "Gym", "Training"],
                "character_count": 287
            },
            "tokens_used": 156
        },
        {
            "user_id": creator.id,
            "request_type": "hashtag_generation",
            "prompt": "Generate 30 relevant hashtags for a protein shake recipe video",
            "response": {
                "hashtags": [
                    "#ProteinShake", "#HealthyRecipes", "#FitnessNutrition", "#MealPrep",
                    "#PostWorkout", "#ProteinRecipe", "#HealthyEating", "#FitFood",
                    "#NutritionTips", "#MuscleBuilding", "#Gains", "#FitnessFood",
                    "#HealthyLifestyle", "#CleanEating", "#FitnessMeal", "#ProteinPacked",
                    "#RecipeIdeas", "#FoodForFuel", "#WorkoutNutrition", "#FitRecipes",
                    "#HealthyDrink", "#SmoothieRecipe", "#FitnessEats", "#MacroFriendly",
                    "#NutritionGoals", "#HighProtein", "#FitLife", "#GymNutrition",
                    "#BodyBuilding", "#FitnessJourney"
                ],
                "total_count": 30,
                "category": "nutrition"
            },
            "tokens_used": 203
        },
        {
            "user_id": coach.id,
            "request_type": "workout_plan",
            "prompt": "Create a 30-minute home workout routine for beginners with no equipment",
            "response": {
                "workout_name": "30-Minute Beginner Home Workout",
                "total_duration": 30,
                "equipment": "None - Bodyweight Only",
                "structure": [
                    {
                        "phase": "Warm-up",
                        "duration": 5,
                        "exercises": [
                            {"name": "Jumping Jacks", "duration": "1 min"},
                            {"name": "Arm Circles", "duration": "1 min"},
                            {"name": "High Knees", "duration": "1 min"},
                            {"name": "Hip Circles", "duration": "1 min"},
                            {"name": "Light Jogging in Place", "duration": "1 min"}
                        ]
                    },
                    {
                        "phase": "Main Workout (3 Rounds)",
                        "duration": 21,
                        "exercises": [
                            {"name": "Push-ups (or knee push-ups)", "reps": "10-12", "rest": "30 sec"},
                            {"name": "Bodyweight Squats", "reps": "15", "rest": "30 sec"},
                            {"name": "Plank Hold", "duration": "30 sec", "rest": "30 sec"},
                            {"name": "Lunges (alternating)", "reps": "10 each leg", "rest": "30 sec"},
                            {"name": "Mountain Climbers", "duration": "30 sec", "rest": "60 sec"}
                        ],
                        "rounds": 3,
                        "rest_between_rounds": "60 seconds"
                    },
                    {
                        "phase": "Cool-down",
                        "duration": 4,
                        "exercises": [
                            {"name": "Standing Quad Stretch", "duration": "30 sec each leg"},
                            {"name": "Hamstring Stretch", "duration": "30 sec each leg"},
                            {"name": "Chest Stretch", "duration": "30 sec"},
                            {"name": "Shoulder Stretch", "duration": "30 sec"},
                            {"name": "Deep Breathing", "duration": "1 min"}
                        ]
                    }
                ],
                "notes": "Focus on proper form over speed. Modify exercises as needed. Stay hydrated!",
                "difficulty": "Beginner",
                "calories_burned_estimate": "200-250"
            },
            "tokens_used": 387
        },
        {
            "user_id": creator.id,
            "request_type": "video_script",
            "prompt": "Write a script for a 2-minute YouTube video about the benefits of morning workouts",
            "response": {
                "title": "Why You NEED to Start Working Out in the Morning",
                "duration": "2 minutes",
                "script": [
                    {
                        "timestamp": "0:00-0:10",
                        "section": "Hook",
                        "dialogue": "What if I told you that working out in the morning could completely transform your life? Not just your body, but your entire day. Let me explain."
                    },
                    {
                        "timestamp": "0:10-0:40",
                        "section": "Benefit 1 - Energy Boost",
                        "dialogue": "First, morning workouts give you an INSTANT energy boost. While others are reaching for their third coffee, you've already got natural endorphins pumping through your system. You'll be more alert, more focused, and ready to crush your day."
                    },
                    {
                        "timestamp": "0:40-1:10",
                        "section": "Benefit 2 - Consistency",
                        "dialogue": "Second, you're way more likely to actually do it. Think about it - how many times have you skipped an evening workout because you were too tired, or something came up? When you train in the morning, it's DONE. No excuses, no distractions. Just you and your goals."
                    },
                    {
                        "timestamp": "1:10-1:40",
                        "section": "Benefit 3 - Mental Clarity",
                        "dialogue": "And finally, the mental benefits are insane. Morning workouts clear your mind, reduce stress, and set a positive tone for the entire day. You're starting with a win, and that momentum carries through everything else you do."
                    },
                    {
                        "timestamp": "1:40-2:00",
                        "section": "Call to Action",
                        "dialogue": "So here's my challenge to you: try it for just ONE week. Wake up 30 minutes earlier and move your body. I guarantee you'll see the difference. If you want a free morning workout routine, check the link in my bio. Now let's get it!"
                    }
                ],
                "visual_notes": [
                    "Show energetic morning workout clips",
                    "Include before/after transformation photos",
                    "Add text overlays for key benefits",
                    "End with subscribe button animation"
                ],
                "background_music": "Upbeat, motivational (120-130 BPM)"
            },
            "tokens_used": 442
        },
        {
            "user_id": coach.id,
            "request_type": "nutrition_plan",
            "prompt": "Create a simple meal plan for muscle gain - 3000 calories, high protein",
            "response": {
                "plan_name": "Muscle Building Meal Plan - 3000 Calories",
                "daily_macros": {
                    "calories": 3000,
                    "protein": "200g (27%)",
                    "carbs": "375g (50%)",
                    "fats": "78g (23%)"
                },
                "meals": [
                    {
                        "meal": "Breakfast (7:00 AM)",
                        "items": [
                            "4 whole eggs, scrambled",
                            "2 slices whole wheat toast",
                            "1 cup oatmeal with berries",
                            "1 banana"
                        ],
                        "macros": {"calories": 720, "protein": "40g", "carbs": "85g", "fats": "22g"}
                    },
                    {
                        "meal": "Mid-Morning Snack (10:00 AM)",
                        "items": [
                            "Protein shake with whole milk",
                            "1 apple",
                            "2 tbsp peanut butter"
                        ],
                        "macros": {"calories": 450, "protein": "35g", "carbs": "45g", "fats": "18g"}
                    },
                    {
                        "meal": "Lunch (1:00 PM)",
                        "items": [
                            "8 oz grilled chicken breast",
                            "2 cups brown rice",
                            "Mixed vegetables",
                            "1 tbsp olive oil for cooking"
                        ],
                        "macros": {"calories": 780, "protein": "60g", "carbs": "90g", "fats": "15g"}
                    },
                    {
                        "meal": "Pre-Workout Snack (4:00 PM)",
                        "items": [
                            "Greek yogurt (1 cup)",
                            "Granola (1/2 cup)",
                            "Honey drizzle"
                        ],
                        "macros": {"calories": 380, "protein": "25g", "carbs": "55g", "fats": "8g"}
                    },
                    {
                        "meal": "Post-Workout Dinner (7:00 PM)",
                        "items": [
                            "8 oz salmon",
                            "Sweet potato (large)",
                            "Broccoli (2 cups)",
                            "Quinoa (1 cup)"
                        ],
                        "macros": {"calories": 670, "protein": "55g", "carbs": "75g", "fats": "15g"}
                    }
                ],
                "notes": [
                    "Drink 1 gallon of water daily",
                    "Adjust portions based on hunger and progress",
                    "Take multivitamin with breakfast",
                    "Optional: 5g creatine daily",
                    "Meal prep on Sundays for the week"
                ],
                "grocery_list": [
                    "Eggs (3 dozen)", "Chicken breast (5 lbs)", "Salmon (2 lbs)",
                    "Brown rice (5 lbs)", "Oatmeal", "Whole wheat bread",
                    "Sweet potatoes", "Broccoli", "Mixed vegetables",
                    "Greek yogurt", "Protein powder", "Peanut butter",
                    "Fruits: bananas, apples, berries", "Olive oil", "Quinoa"
                ]
            },
            "tokens_used": 521
        },
        {
            "user_id": creator.id,
            "request_type": "content_ideas",
            "prompt": "Give me 10 viral video ideas for fitness TikTok",
            "response": {
                "ideas": [
                    {
                        "title": "Gym Equipment Hacks Nobody Knows",
                        "description": "Show 5 unconventional ways to use common gym equipment",
                        "hook": "Your gym has been hiding these tricks from you...",
                        "viral_potential": "High"
                    },
                    {
                        "title": "Try This Before Every Workout",
                        "description": "3-minute dynamic warm-up routine that prevents injuries",
                        "hook": "This 3-minute warm-up will change your workouts forever",
                        "viral_potential": "Medium-High"
                    },
                    {
                        "title": "Gym Red Flags 🚩",
                        "description": "Funny compilation of bad gym etiquette and form",
                        "hook": "If your gym buddy does this... RUN 🚩",
                        "viral_potential": "Very High"
                    },
                    {
                        "title": "Home vs Gym: Same Workout",
                        "description": "Side-by-side comparison showing home alternatives",
                        "hook": "You don't need a gym membership for this...",
                        "viral_potential": "High"
                    },
                    {
                        "title": "Bulking vs Cutting Transformation",
                        "description": "Time-lapse showing body changes in both phases",
                        "hook": "Watch my body transform in 60 seconds",
                        "viral_potential": "Very High"
                    },
                    {
                        "title": "Myths Personal Trainers Want You to Believe",
                        "description": "Debunk 5 common fitness myths with science",
                        "hook": "Personal trainers don't want you to know this...",
                        "viral_potential": "High"
                    },
                    {
                        "title": "Rating Gym Chains",
                        "description": "Visit and review 5 different gym franchises",
                        "hook": "I tried EVERY major gym chain so you don't have to",
                        "viral_potential": "Medium-High"
                    },
                    {
                        "title": "Follow My Exact Routine",
                        "description": "Full day of eating + training for muscle gain",
                        "hook": "Do THIS to gain 10 lbs of muscle",
                        "viral_potential": "Very High"
                    },
                    {
                        "title": "Gym Fails Reaction",
                        "description": "React to viral gym fail videos, explain what went wrong",
                        "hook": "Reacting to the WORST gym fails on the internet",
                        "viral_potential": "Very High"
                    },
                    {
                        "title": "Challenge: $1 vs $100 Protein",
                        "description": "Blind taste test and nutrition comparison",
                        "hook": "Is expensive protein actually better?",
                        "viral_potential": "Medium"
                    }
                ],
                "posting_tips": [
                    "Post at 6-8 PM for best engagement",
                    "Use trending audio when possible",
                    "First 3 seconds are CRITICAL - hook immediately",
                    "Include text overlays for accessibility",
                    "Reply to top comments within 1 hour"
                ]
            },
            "tokens_used": 489
        }
    ]

    ai_requests = []
    for request_data in ai_requests_data:
        ai_request = AIRequest(**request_data)
        db.add(ai_request)
        ai_requests.append(ai_request)

    db.commit()

    for request in ai_requests:
        db.refresh(request)

    print(f"✓ Created {len(ai_requests)} AI requests")
    request_types = {}
    for request in ai_requests:
        request_types[request.request_type] = request_types.get(request.request_type, 0) + 1
    for req_type, count in request_types.items():
        print(f"  - {req_type}: {count}")
    print(f"  - Total tokens used: {sum(r.tokens_used for r in ai_requests):,}")
    print()

    return ai_requests


def main():
    """Main seeding function"""
    print("\n" + "="*60)
    print("🌱 CREATORSAPP - DATABASE SEEDING SCRIPT")
    print("="*60 + "\n")

    # Create database session
    db = SessionLocal()

    try:
        # Ask for confirmation before clearing data
        response = input("⚠️  This will CLEAR all existing data. Continue? (yes/no): ")
        if response.lower() != 'yes':
            print("❌ Seeding cancelled.")
            return

        print()

        # Clear existing data
        clear_all_data(db)

        # Seed all data
        users = seed_users(db)
        projects = seed_projects(db, users)
        tasks = seed_tasks(db, projects)
        risks = seed_risks(db, projects)
        posts = seed_posts(db, users, projects)
        ai_requests = seed_ai_requests(db, users)

        print("="*60)
        print("✅ DATABASE SEEDING COMPLETED SUCCESSFULLY!")
        print("="*60)
        print("\n📊 Summary:")
        print(f"  - Users: {len(users)}")
        print(f"  - Projects: {len(projects)}")
        print(f"  - Tasks: {len(tasks)}")
        print(f"  - Risks: {len(risks)}")
        print(f"  - Posts: {len(posts)}")
        print(f"  - AI Requests: {len(ai_requests)}")
        print("\n🔑 Test User Credentials:")
        print("  Admin:   admin@creatorsapp.com / Admin123!")
        print("  Coach:   coach@fitness.com / Coach123!")
        print("  Creator: creator@youtube.com / Creator123!")
        print("  User:    user@example.com / User123!")
        print("\n🚀 You can now login and explore the app!")
        print()

    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()

"""
Seed data for JerryGFit - Fitness Content Creator Platform
Creates realistic demo data for all models to showcase features
"""

import asyncio
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.database import SessionLocal
from app.models.user import User, UserRole
from app.models.project import Project, ProjectStatus
from app.models.task import Task, TaskStatus, TaskPriority
from app.models.risk import Risk, RiskSeverity, RiskStatus, RiskProbability, RiskImpact
from app.models.post import Post
from app.models.ai_request import AIRequest

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def clear_database(db: Session):
    """Clear all existing data"""
    print("🗑️  Clearing existing data...")

    # Delete in reverse order of dependencies
    db.query(AIRequest).delete()
    db.query(Post).delete()
    db.query(Risk).delete()
    db.query(Task).delete()
    db.query(Project).delete()
    db.query(User).delete()

    db.commit()
    print("✅ Database cleared!")

def seed_users(db: Session):
    """Create demo users with different roles"""
    print("\n👥 Creating users...")

    users = [
        User(
            email="jerry@jerrygfit.com",
            username="jerrygfit",
            full_name="Jerry Thompson",
            hashed_password=get_password_hash("Jerry123!"),
            role=UserRole.ADMIN,
            is_active=True,
            notification_preferences={"email": True, "push": True, "sms": False},
            user_preferences={"theme": "dark", "language": "en"}
        ),
        User(
            email="sarah@jerrygfit.com",
            username="sarahfit",
            full_name="Sarah Martinez",
            hashed_password=get_password_hash("Sarah123!"),
            role=UserRole.CREATOR,
            is_active=True,
            notification_preferences={"email": True, "push": True, "sms": False},
            user_preferences={"theme": "dark", "language": "en"}
        ),
        User(
            email="mike@jerrygfit.com",
            username="mikewellness",
            full_name="Mike Chen",
            hashed_password=get_password_hash("Mike123!"),
            role=UserRole.COACH,
            is_active=True,
            notification_preferences={"email": True, "push": False, "sms": False},
            user_preferences={"theme": "light", "language": "en"}
        ),
        User(
            email="alex@client.com",
            username="alexviewer",
            full_name="Alex Johnson",
            hashed_password=get_password_hash("Alex123!"),
            role=UserRole.USER,
            is_active=True,
            notification_preferences={"email": True, "push": False, "sms": False},
            user_preferences={"theme": "dark", "language": "en"}
        ),
    ]

    for user in users:
        db.add(user)

    db.commit()
    for user in users:
        db.refresh(user)

    print(f"✅ Created {len(users)} users")
    return users

def seed_projects(db: Session, users: list):
    """Create fitness content projects"""
    print("\n📁 Creating projects...")

    owner = users[0]
    today = datetime.now(timezone.utc)

    projects = [
        Project(
            name="January Transformation Challenge",
            description="30-day fitness transformation challenge with daily workout videos, meal plans, and progress tracking. Target: 50k views, 1000 new subscribers.",
            status=ProjectStatus.ACTIVE,
            due_date=today + timedelta(days=15),
            progress=60.0,
            owner_id=owner.id
        ),
        Project(
            name="Summer Shred Series 2024",
            description="12-week intensive training program focused on fat loss and muscle definition. Includes workout routines, nutrition guides, and weekly check-ins.",
            status=ProjectStatus.ACTIVE,
            due_date=today + timedelta(days=90),
            progress=15.0,
            owner_id=owner.id
        ),
        Project(
            name="Beginner's Guide to Strength Training",
            description="Comprehensive beginner series covering proper form, progressive overload, and building a sustainable routine. 8-week program with video tutorials.",
            status=ProjectStatus.ACTIVE,
            due_date=today + timedelta(days=45),
            progress=75.0,
            owner_id=owner.id
        ),
        Project(
            name="Nutrition Fundamentals Course",
            description="Online course about macronutrients, meal prep, and sustainable eating habits. Partnering with registered dietitians.",
            status=ProjectStatus.ON_HOLD,
            due_date=today + timedelta(days=120),
            progress=25.0,
            owner_id=owner.id
        ),
        Project(
            name="Holiday Workout Series",
            description="Quick home workouts for busy holiday season. 10-20 minute sessions, no equipment needed. High-volume content push.",
            status=ProjectStatus.COMPLETED,
            due_date=today - timedelta(days=10),
            progress=100.0,
            owner_id=owner.id
        ),
    ]

    for project in projects:
        db.add(project)

    db.commit()
    for project in projects:
        db.refresh(project)

    print(f"✅ Created {len(projects)} projects")
    return projects

def seed_tasks(db: Session, projects: list, users: list):
    """Create realistic tasks for projects"""
    print("\n✅ Creating tasks...")

    owner = users[0]
    sarah = users[1]
    today = datetime.now(timezone.utc)

    tasks = [
        # January Transformation Challenge tasks
        Task(
            title="Plan 30-day workout schedule",
            description="Create detailed workout plan with daily exercises, rest days, and progression",
            status=TaskStatus.DONE,
            priority=TaskPriority.HIGH,
            owner_id=owner.id,
            due_date=today - timedelta(days=10),
            completed=True
        ),
        Task(
            title="Film intro and welcome video",
            description="Record professional welcome video explaining challenge rules and expectations",
            status=TaskStatus.DONE,
            priority=TaskPriority.HIGH,
            owner_id=sarah.id,
            due_date=today - timedelta(days=8),
            completed=True
        ),
        Task(
            title="Create progress tracking spreadsheet",
            description="Design template for participants to log workouts and measurements",
            status=TaskStatus.IN_PROGRESS,
            priority=TaskPriority.MEDIUM,
            owner_id=owner.id,
            due_date=today + timedelta(days=2),
            completed=False
        ),
        Task(
            title="Edit Week 3 workout videos",
            description="Edit and upload videos for days 15-21 of the challenge",
            status=TaskStatus.IN_PROGRESS,
            priority=TaskPriority.HIGH,
            owner_id=sarah.id,
            due_date=today + timedelta(days=3),
            completed=False
        ),
        Task(
            title="Design challenge completion certificate",
            description="Create digital certificate for participants who complete all 30 days",
            status=TaskStatus.TODO,
            priority=TaskPriority.LOW,
            owner_id=sarah.id,
            due_date=today + timedelta(days=12),
            completed=False
        ),

        # Summer Shred Series tasks
        Task(
            title="Outline 12-week program structure",
            description="Break down training phases and progression for the entire series",
            status=TaskStatus.DONE,
            priority=TaskPriority.HIGH,
            owner_id=owner.id,
            due_date=today - timedelta(days=5),
            completed=True
        ),
        Task(
            title="Film Week 1 training videos",
            description="Record all workouts for week 1 with proper demonstrations",
            status=TaskStatus.IN_PROGRESS,
            priority=TaskPriority.HIGH,
            owner_id=owner.id,
            due_date=today + timedelta(days=7),
            completed=False
        ),
        Task(
            title="Create meal prep guide PDF",
            description="Design downloadable nutrition guide with recipes and shopping lists",
            status=TaskStatus.TODO,
            priority=TaskPriority.MEDIUM,
            owner_id=owner.id,
            due_date=today + timedelta(days=14),
            completed=False
        ),

        # Beginner's Guide tasks
        Task(
            title="Finalize exercise library",
            description="Complete database of beginner-friendly exercises with video demonstrations",
            status=TaskStatus.DONE,
            priority=TaskPriority.HIGH,
            owner_id=owner.id,
            due_date=today - timedelta(days=20),
            completed=True
        ),
        Task(
            title="Write safety and form guide",
            description="Create comprehensive guide on proper form, common mistakes, and injury prevention",
            status=TaskStatus.DONE,
            priority=TaskPriority.HIGH,
            owner_id=owner.id,
            due_date=today - timedelta(days=15),
            completed=True
        ),
        Task(
            title="Upload Week 7 content",
            description="Final week of content upload with progressive overload techniques",
            status=TaskStatus.IN_PROGRESS,
            priority=TaskPriority.HIGH,
            owner_id=sarah.id,
            due_date=today + timedelta(days=5),
            completed=False
        ),
        Task(
            title="Create beginner FAQ document",
            description="Compile frequently asked questions and detailed answers",
            status=TaskStatus.TODO,
            priority=TaskPriority.MEDIUM,
            owner_id=owner.id,
            due_date=today + timedelta(days=10),
            completed=False
        ),
    ]

    for task in tasks:
        db.add(task)

    db.commit()
    print(f"✅ Created {len(tasks)} tasks")
    return tasks

def seed_risks(db: Session, users: list):
    """Create risk entries"""
    print("\n⚠️  Creating risks...")

    owner = users[0]
    today = datetime.now(timezone.utc)

    risks = [
        Risk(
            title="YouTube Algorithm Changes",
            description="Recent algorithm updates may reduce reach for fitness content. Need to adapt content strategy and optimize for new ranking factors.",
            severity=RiskSeverity.HIGH,
            probability=RiskProbability.MEDIUM,
            impact=RiskImpact.HIGH,
            status=RiskStatus.OPEN,
            mitigation_plan="Diversify content across multiple platforms (Instagram, TikTok). Focus on shorts/reels. Increase community engagement.",
            owner_id=owner.id
        ),
        Risk(
            title="Equipment Shortage for Filming",
            description="Main camera equipment scheduled for maintenance. Backup camera has lower quality which may affect content standards.",
            severity=RiskSeverity.MEDIUM,
            probability=RiskProbability.LOW,
            impact=RiskImpact.MEDIUM,
            status=RiskStatus.MITIGATED,
            mitigation_plan="Rented professional equipment for 2 weeks. Adjusted filming schedule to batch-create content.",
            owner_id=owner.id
        ),
        Risk(
            title="Increased Competition in Fitness Content",
            description="Multiple new fitness creators entering the space with similar content themes. Market saturation could impact growth.",
            severity=RiskSeverity.MEDIUM,
            probability=RiskProbability.HIGH,
            impact=RiskImpact.MEDIUM,
            status=RiskStatus.OPEN,
            mitigation_plan="Focus on unique personal brand and authentic storytelling. Develop signature workout series. Increase production quality.",
            owner_id=owner.id
        ),
        Risk(
            title="Seasonal Viewership Decline",
            description="Historical data shows 30% drop in fitness content engagement during summer months when people are more active outdoors.",
            severity=RiskSeverity.LOW,
            probability=RiskProbability.HIGH,
            impact=RiskImpact.LOW,
            status=RiskStatus.MITIGATED,
            mitigation_plan="Created outdoor workout content. Planning summer-specific challenges. Scheduled content buffer during peak months.",
            owner_id=owner.id
        ),
        Risk(
            title="Copyright Strike on Music",
            description="Risk of copyright claims on background music used in workout videos. Could result in video takedowns or channel strikes.",
            severity=RiskSeverity.CRITICAL,
            probability=RiskProbability.LOW,
            impact=RiskImpact.CRITICAL,
            status=RiskStatus.MITIGATED,
            mitigation_plan="Switched to royalty-free music library. Reviewing all existing content for compliance. Using YouTube Audio Library.",
            owner_id=owner.id
        ),
    ]

    for risk in risks:
        db.add(risk)

    db.commit()
    print(f"✅ Created {len(risks)} risks")
    return risks

def seed_posts(db: Session, projects: list, users: list):
    """Create social media posts"""
    print("\n📱 Creating posts...")

    owner = users[0]
    today = datetime.now(timezone.utc)

    posts = [
        Post(
            title="Day 1 - Transformation Challenge Begins!",
            content="Welcome to the 30-Day Transformation Challenge! Today we're starting with a full-body assessment workout...",
            caption="🔥 Who's ready to transform? Drop a 💪 if you're joining the challenge! #FitnessChallenge #Transformation",
            hashtags="#fitness #workout #transformation #30daychallenge #fitnessmotivation #gym #health",
            likes=1247,
            comments=183,
            shares=94,
            engagement_rate=12.2,
            project_id=projects[0].id,
            user_id=owner.id,
            published_at=today - timedelta(days=15)
        ),
        Post(
            title="Week 1 Results - Amazing Progress!",
            content="One week down! Here are some incredible transformations from our community...",
            caption="The results are already showing! Keep pushing 💯 #WeekOneComplete",
            hashtags="#fitnessjourney #results #beforeandafter #fitfam #motivation",
            likes=2893,
            comments=412,
            shares=267,
            engagement_rate=15.7,
            project_id=projects[0].id,
            user_id=owner.id,
            published_at=today - timedelta(days=8)
        ),
        Post(
            title="Proper Squat Form Tutorial",
            content="Master the squat! This video breaks down every aspect of proper squat technique...",
            caption="Foundation first 🏗️ Perfect your form before adding weight! Save this for later 🔖",
            hashtags="#squats #formcheck #strengthtraining #beginnerfitness #technique",
            likes=5621,
            comments=289,
            shares=432,
            engagement_rate=18.4,
            project_id=projects[2].id,
            user_id=owner.id,
            published_at=today - timedelta(days=12)
        ),
        Post(
            title="Summer Shred Announcement",
            content="Exciting news! The Summer Shred Series starts next month. 12 weeks of intense training...",
            caption="🌞 Summer bodies are built in spring! Who's in? Registration opens tomorrow ⚡",
            hashtags="#summershred #fitnessprogram #summerready #workout #training",
            likes=3429,
            comments=567,
            shares=189,
            engagement_rate=14.8,
            project_id=projects[1].id,
            user_id=owner.id,
            published_at=today - timedelta(days=5)
        ),
        Post(
            title="Meal Prep Basics",
            content="Nutrition is 70% of the battle! Here's my Sunday meal prep routine for the week...",
            caption="Sunday prep = Weekly success 🥗 What's your go-to meal prep? Comment below!",
            hashtags="#mealprep #nutrition #healthyeating #fitmeal #wellness",
            likes=4782,
            comments=625,
            shares=412,
            engagement_rate=16.9,
            project_id=projects[3].id,
            user_id=owner.id,
            published_at=today - timedelta(days=3)
        ),
        Post(
            title="Holiday Workouts Wrap-Up",
            content="Thank you to everyone who joined the holiday workout series! Over 50,000 of you stayed active...",
            caption="You all crushed it! 🎉 Stats: 50K participants, 2M total workout minutes 💪",
            hashtags="#fitnesscommunity #thankyou #holidays #stayactive #results",
            likes=8934,
            comments=1203,
            shares=678,
            engagement_rate=21.3,
            project_id=projects[4].id,
            user_id=owner.id,
            published_at=today - timedelta(days=25)
        ),
    ]

    for post in posts:
        db.add(post)

    db.commit()
    print(f"✅ Created {len(posts)} posts")
    return posts

def seed_ai_requests(db: Session, users: list):
    """Create AI request history"""
    print("\n🤖 Creating AI requests...")

    owner = users[0]
    today = datetime.now(timezone.utc)

    ai_requests = [
        AIRequest(
            user_id=owner.id,
            request_type="content_generation",
            prompt="Generate 5 engaging Instagram captions for a workout video about leg day",
            response={
                "captions": [
                    "Leg day = best day 💪 Who else loves the burn?",
                    "Never skip leg day! Drop a 🔥 if you're training legs today",
                    "Building a strong foundation, one rep at a time 🏗️",
                    "The only bad workout is the one you didn't do. Let's get it!",
                    "Leg day complete ✅ Who's ready for the weekend?"
                ]
            },
            tokens_used=487
        ),
        AIRequest(
            user_id=owner.id,
            request_type="hashtag_suggestions",
            prompt="Suggest 20 trending hashtags for fitness transformation content",
            response={
                "hashtags": [
                    "#transformation", "#fitnessmotivation", "#beforeandafter",
                    "#fitnessjourney", "#weightloss", "#muscle", "#gains"
                ]
            },
            tokens_used=312
        ),
        AIRequest(
            user_id=owner.id,
            request_type="video_script",
            prompt="Write a 60-second video script for introducing a 30-day fitness challenge",
            response={
                "script": "Hey everyone! I'm so excited to announce our 30-Day Transformation Challenge..."
            },
            tokens_used=856
        ),
    ]

    for ai_request in ai_requests:
        db.add(ai_request)

    db.commit()
    print(f"✅ Created {len(ai_requests)} AI requests")
    return ai_requests

def main():
    """Main seeding function"""
    print("🌱 Starting database seeding for JerryGFit...\n")
    print("=" * 60)

    db = SessionLocal()

    try:
        # Clear existing data
        clear_database(db)

        # Seed data in order
        users = seed_users(db)
        projects = seed_projects(db, users)
        tasks = seed_tasks(db, projects, users)
        risks = seed_risks(db, users)
        posts = seed_posts(db, projects, users)
        ai_requests = seed_ai_requests(db, users)

        print("\n" + "=" * 60)
        print("✅ Database seeding completed successfully!")
        print("\n📊 Summary:")
        print(f"   • Users: {len(users)}")
        print(f"   • Projects: {len(projects)}")
        print(f"   • Tasks: {len(tasks)}")
        print(f"   • Risks: {len(risks)}")
        print(f"   • Posts: {len(posts)}")
        print(f"   • AI Requests: {len(ai_requests)}")
        print("\n🔐 Test Accounts:")
        print("   • Admin: jerry@jerrygfit.com / Jerry123!")
        print("   • Creator: sarah@jerrygfit.com / Sarah123!")
        print("   • Coach: mike@jerrygfit.com / Mike123!")
        print("   • User: alex@client.com / Alex123!")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ Error during seeding: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()

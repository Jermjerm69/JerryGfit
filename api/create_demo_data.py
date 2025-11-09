#!/usr/bin/env python3
"""
Create comprehensive demo data
Populates the database with realistic test data for demo purposes
"""

import requests
import json
from datetime import datetime, timedelta
import random

BASE_URL = "http://localhost:8000/api/v1"

# Demo user credentials
DEMO_EMAIL = "demo@jerrygfit.com"
DEMO_PASSWORD = "Demo12345"

def create_demo_user():
    """Create a demo user"""
    print("\n" + "="*60)
    print("Creating Demo User...")
    print("="*60)

    user_data = {
        "email": DEMO_EMAIL,
        "username": "demo",
        "password": DEMO_PASSWORD,
        "full_name": "Demo User"
    }

    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=user_data)
        if response.status_code == 201:
            print(f"✅ Demo user created: {DEMO_EMAIL}")
            return True
        elif response.status_code == 400 and "already registered" in response.text:
            print(f"ℹ️  Demo user already exists: {DEMO_EMAIL}")
            return True
        else:
            print(f"❌ Failed to create demo user: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error creating demo user: {e}")
        return False

def login_demo_user():
    """Login and get access token"""
    print("\nLogging in as demo user...")

    login_data = {
        "username": DEMO_EMAIL,
        "password": DEMO_PASSWORD
    }

    try:
        response = requests.post(
            f"{BASE_URL}/auth/login",
            data=login_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )

        if response.status_code == 200:
            result = response.json()
            access_token = result.get("access_token")
            print(f"✅ Logged in successfully")
            return access_token
        else:
            print(f"❌ Login failed: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error logging in: {e}")
        return None

def create_tasks(headers):
    """Create demo tasks"""
    print("\n" + "="*60)
    print("Creating Tasks...")
    print("="*60)

    tasks = [
        {
            "title": "Design new workout program",
            "description": "Create a comprehensive 12-week strength training program for intermediate lifters",
            "status": "done",
            "priority": "high",
            "due_date": (datetime.now() - timedelta(days=5)).isoformat()
        },
        {
            "title": "Film tutorial videos",
            "description": "Record form check videos for all major compound movements",
            "status": "in_progress",
            "priority": "high",
            "due_date": (datetime.now() + timedelta(days=3)).isoformat()
        },
        {
            "title": "Edit Instagram reels",
            "description": "Edit and schedule 10 reels for the upcoming week",
            "status": "todo",
            "priority": "medium",
            "due_date": (datetime.now() + timedelta(days=7)).isoformat()
        },
        {
            "title": "Update nutrition guide",
            "description": "Revise macro calculations and meal planning section",
            "status": "todo",
            "priority": "low",
            "due_date": (datetime.now() + timedelta(days=14)).isoformat()
        },
        {
            "title": "Client consultation - Sarah",
            "description": "Initial fitness assessment and goal setting session",
            "status": "done",
            "priority": "urgent",
            "due_date": (datetime.now() - timedelta(days=2)).isoformat()
        },
        {
            "title": "Research new supplements",
            "description": "Evaluate latest research on creatine alternatives",
            "status": "blocked",
            "priority": "low",
            "due_date": (datetime.now() + timedelta(days=21)).isoformat()
        },
        {
            "title": "Plan group training session",
            "description": "Design circuit workout for Saturday bootcamp class",
            "status": "in_progress",
            "priority": "medium",
            "due_date": (datetime.now() + timedelta(days=2)).isoformat()
        },
        {
            "title": "Create meal prep content",
            "description": "Batch cook and document 5 high-protein meal recipes",
            "status": "todo",
            "priority": "medium",
            "due_date": (datetime.now() + timedelta(days=10)).isoformat()
        }
    ]

    created_count = 0
    for task_data in tasks:
        try:
            response = requests.post(f"{BASE_URL}/tasks", json=task_data, headers=headers)
            if response.status_code == 200:
                created_count += 1
                print(f"✅ Created task: {task_data['title']}")
            else:
                print(f"❌ Failed to create task: {task_data['title']}")
        except Exception as e:
            print(f"❌ Error creating task: {e}")

    print(f"\n📊 Created {created_count}/{len(tasks)} tasks")
    return created_count

def create_risks(headers):
    """Create demo risks"""
    print("\n" + "="*60)
    print("Creating Risks...")
    print("="*60)

    risks = [
        {
            "title": "Equipment failure during live stream",
            "description": "Camera or lighting equipment may malfunction during a scheduled live workout session",
            "severity": "high",
            "probability": "low",
            "impact": "high",
            "status": "open",
            "mitigation_plan": "Have backup equipment ready, test all gear 30 minutes before going live, keep a backup phone camera charged"
        },
        {
            "title": "Content copyright issues",
            "description": "Using copyrighted music in video content could lead to takedowns or strikes",
            "severity": "critical",
            "probability": "medium",
            "impact": "critical",
            "status": "mitigated",
            "mitigation_plan": "Only use royalty-free music from licensed libraries, maintain spreadsheet of licensed tracks, watermark all original content"
        },
        {
            "title": "Client injury liability",
            "description": "A client could get injured following online workout programs without proper form supervision",
            "severity": "critical",
            "probability": "low",
            "impact": "critical",
            "status": "mitigated",
            "mitigation_plan": "Require signed liability waivers, include disclaimers in all content, maintain professional liability insurance, emphasize proper form in all videos"
        },
        {
            "title": "Algorithm changes affecting reach",
            "description": "Social media platform algorithm updates may decrease organic reach and engagement",
            "severity": "high",
            "probability": "high",
            "impact": "medium",
            "status": "open",
            "mitigation_plan": "Diversify across multiple platforms, build email list, engage consistently with community, adapt content strategy based on analytics"
        },
        {
            "title": "Burnout from content creation",
            "description": "Maintaining daily content schedule may lead to creator burnout and decreased quality",
            "severity": "medium",
            "probability": "medium",
            "impact": "medium",
            "status": "open",
            "mitigation_plan": "Batch content creation sessions, schedule rest days, delegate editing work, maintain content calendar 2 weeks ahead"
        },
        {
            "title": "Competition from new fitness influencers",
            "description": "Market saturation with new fitness content creators may reduce audience growth",
            "severity": "medium",
            "probability": "high",
            "impact": "low",
            "status": "open",
            "mitigation_plan": "Focus on unique value proposition, build strong community engagement, continuously improve content quality, collaborate with complementary creators"
        }
    ]

    created_count = 0
    for risk_data in risks:
        try:
            response = requests.post(f"{BASE_URL}/risks", json=risk_data, headers=headers)
            if response.status_code == 200:
                created_count += 1
                print(f"✅ Created risk: {risk_data['title']}")
            else:
                print(f"❌ Failed to create risk: {risk_data['title']} - {response.text}")
        except Exception as e:
            print(f"❌ Error creating risk: {e}")

    print(f"\n📊 Created {created_count}/{len(risks)} risks")
    return created_count

def create_projects(headers):
    """Create demo projects"""
    print("\n" + "="*60)
    print("Creating Projects...")
    print("="*60)

    projects = [
        {
            "name": "Q1 2025 Content Strategy",
            "description": "Comprehensive content plan for January-March including video series, blog posts, and social media campaigns",
            "status": "active",
            "progress": 65.0,
            "due_date": (datetime.now() + timedelta(days=90)).isoformat()
        },
        {
            "name": "Online Coaching Program Launch",
            "description": "Develop and launch premium 1-on-1 online coaching service with custom workout and nutrition plans",
            "status": "active",
            "progress": 40.0,
            "due_date": (datetime.now() + timedelta(days=45)).isoformat()
        },
        {
            "name": "YouTube Channel Rebranding",
            "description": "Update channel branding, create new intro/outro, redesign thumbnails for consistency",
            "status": "active",
            "progress": 85.0,
            "due_date": (datetime.now() + timedelta(days=15)).isoformat()
        },
        {
            "name": "Fitness App Development",
            "description": "Partner with developers to create branded fitness tracking mobile app",
            "status": "on_hold",
            "progress": 20.0,
            "due_date": (datetime.now() + timedelta(days=180)).isoformat()
        },
        {
            "name": "Summer Shred Challenge",
            "description": "8-week community fitness challenge with daily workouts, nutrition tips, and prizes",
            "status": "completed",
            "progress": 100.0,
            "due_date": (datetime.now() - timedelta(days=30)).isoformat()
        }
    ]

    created_count = 0
    for project_data in projects:
        try:
            response = requests.post(f"{BASE_URL}/projects", json=project_data, headers=headers)
            if response.status_code == 200:
                created_count += 1
                print(f"✅ Created project: {project_data['name']}")
            else:
                print(f"❌ Failed to create project: {project_data['name']}")
        except Exception as e:
            print(f"❌ Error creating project: {e}")

    print(f"\n📊 Created {created_count}/{len(projects)} projects")
    return created_count

def create_ai_generations(headers):
    """Create some AI generation history"""
    print("\n" + "="*60)
    print("Generating AI Content...")
    print("="*60)

    prompts = [
        {
            "request_type": "caption",
            "prompt": "Create an inspiring caption about leg day and pushing through challenges",
            "model": "gpt-4"
        },
        {
            "request_type": "hashtag",
            "prompt": "Generate trending hashtags for a home workout video targeting busy professionals",
            "model": "gpt-4"
        },
        {
            "request_type": "workout_plan",
            "prompt": "Design a 30-minute upper body dumbbell workout for beginners",
            "model": "gpt-4"
        }
    ]

    created_count = 0
    for prompt_data in prompts:
        try:
            response = requests.post(f"{BASE_URL}/ai/generate", json=prompt_data, headers=headers)
            if response.status_code == 200:
                created_count += 1
                result = response.json()
                print(f"✅ Generated: {prompt_data['request_type']} ({result.get('tokens_used', 0)} tokens)")
            else:
                print(f"⚠️  AI generation skipped (OpenAI key may not be configured)")
                break  # Skip remaining if API key not configured
        except Exception as e:
            print(f"⚠️  AI generation skipped: {e}")
            break

    print(f"\n📊 Generated {created_count}/{len(prompts)} AI contents")
    return created_count

def main():
    """Main function to create all demo data"""
    print("\n" + "="*80)
    print("🏋️  JERRYGFIT DEMO DATA GENERATOR")
    print("="*80)

    # Step 1: Create demo user
    if not create_demo_user():
        print("\n❌ Failed to create demo user. Exiting...")
        return

    # Step 2: Login
    access_token = login_demo_user()
    if not access_token:
        print("\n❌ Failed to login. Exiting...")
        return

    headers = {"Authorization": f"Bearer {access_token}"}

    # Step 3: Create demo data
    tasks_created = create_tasks(headers)
    risks_created = create_risks(headers)
    projects_created = create_projects(headers)
    ai_created = create_ai_generations(headers)

    # Final summary
    print("\n" + "="*80)
    print("📊 DEMO DATA CREATION SUMMARY")
    print("="*80)
    print(f"✅ User: {DEMO_EMAIL} (password: {DEMO_PASSWORD})")
    print(f"✅ Tasks Created: {tasks_created}")
    print(f"✅ Risks Created: {risks_created}")
    print(f"✅ Projects Created: {projects_created}")
    print(f"✅ AI Generations: {ai_created}")
    print("\n🎉 Demo data creation complete!")
    print(f"\n🔗 Login at: http://localhost:3000/auth/login")
    print(f"   Email: {DEMO_EMAIL}")
    print(f"   Password: {DEMO_PASSWORD}")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()

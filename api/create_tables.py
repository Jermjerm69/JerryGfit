"""
Quick script to create all database tables.
Run this before seed.py if Alembic isn't working.

Usage:
    python create_tables.py
"""

from app.database import Base, engine
from app.models.user import User
from app.models.risk import Risk
from app.models.task import Task
from app.models.engagement_metric import EngagementMetric
from app.models.ai_request import AIRequest

def create_tables():
    """Create all tables in the database."""
    try:
        print("Creating database tables...")

        # Import all models so they're registered with Base
        # This ensures all tables are created

        # Create all tables
        Base.metadata.create_all(bind=engine)

        print("✅ All tables created successfully!")
        print("\nCreated tables:")
        print("  - users")
        print("  - risks")
        print("  - tasks")
        print("  - engagement_metrics")
        print("  - ai_requests")
        print("\nYou can now run: python seed.py")

    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    create_tables()

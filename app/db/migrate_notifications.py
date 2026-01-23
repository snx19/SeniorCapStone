"""Migration script to add notifications table and dispute fields."""
from app.db.session import SessionLocal
from app.db.base import Base, engine
from sqlalchemy import text

# Import models to ensure they're registered
from app.db.models import Notification, Exam

def migrate_notifications():
    """Create notifications table and add dispute fields to exams table."""
    db = SessionLocal()
    
    try:
        print("=" * 80)
        print("MIGRATING - Adding Notifications and Dispute Functionality")
        print("=" * 80)
        
        # Create notifications table
        print("\nCreating notifications table...")
        try:
            Base.metadata.create_all(bind=engine, tables=[Notification.__table__])
            print("  [+] Notifications table created")
        except Exception as e:
            print(f"  [X] Error creating notifications table: {e}")
            # Try manual creation
            try:
                db.execute(text("""
                    CREATE TABLE IF NOT EXISTS notifications (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        notification_type VARCHAR(50) NOT NULL,
                        title VARCHAR(255) NOT NULL,
                        message TEXT NOT NULL,
                        related_exam_id INTEGER,
                        related_course_id INTEGER,
                        is_read BOOLEAN DEFAULT 0 NOT NULL,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users(id),
                        FOREIGN KEY (related_exam_id) REFERENCES exams(id),
                        FOREIGN KEY (related_course_id) REFERENCES courses(id)
                    )
                """))
                db.execute(text("CREATE INDEX IF NOT EXISTS ix_notifications_user_id ON notifications(user_id)"))
                db.commit()
                print("  [+] Notifications table created manually")
            except Exception as e2:
                print(f"  [X] Error creating notifications table manually: {e2}")
                db.rollback()
        
        # Add dispute_reason column to exams table
        print("\nAdding dispute_reason column to exams table...")
        try:
            result = db.execute(text(
                "SELECT COUNT(*) as count FROM pragma_table_info('exams') WHERE name='dispute_reason'"
            ))
            exists = result.fetchone()[0] > 0
            
            if not exists:
                print("  [+] Adding column: dispute_reason")
                db.execute(text("ALTER TABLE exams ADD COLUMN dispute_reason TEXT"))
                db.commit()
                print("  [+] dispute_reason column added")
            else:
                print("  [-] Column dispute_reason already exists, skipping")
        except Exception as e:
            print(f"  [X] Error adding dispute_reason column: {e}")
            db.rollback()
        
        print("\n[SUCCESS] Migration complete!")
        print("\n" + "=" * 80)
        
    except Exception as e:
        print(f"\n[ERROR] Error during migration: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    migrate_notifications()

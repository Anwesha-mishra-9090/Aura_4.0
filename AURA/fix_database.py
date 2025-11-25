import os
import sqlite3


def fix_database():
    """Fix corrupted database by creating a new one"""
    print("🔧 Fixing AURA Database...")

    db_file = 'aura.db'
    backup_file = 'aura.db.backup'

    # Remove corrupted database
    if os.path.exists(db_file):
        try:
            # Try to backup corrupted file
            if os.path.exists(backup_file):
                os.remove(backup_file)
            os.rename(db_file, backup_file)
            print("✅ Created backup of corrupted database")
        except Exception as e:
            print(f"⚠️  Could not backup corrupted database: {e}")
            try:
                os.remove(db_file)
                print("🗑️  Removed corrupted database file")
            except:
                print("❌ Could not remove corrupted database file")
                return False
    else:
        print("📁 No existing database found - will create new one")

    # Test creating new database
    try:
        conn = sqlite3.connect(db_file)
        conn.execute("CREATE TABLE IF NOT EXISTS test (id INTEGER PRIMARY KEY)")
        conn.execute("DROP TABLE test")
        conn.close()
        print("✅ New database created successfully")
        return True
    except Exception as e:
        print(f"❌ Could not create new database: {e}")
        return False


if __name__ == "__main__":
    if fix_database():
        print("\n🎯 Database fixed! Now run: python main.py")
    else:
        print("\n❌ Database fix failed. Please check file permissions.")
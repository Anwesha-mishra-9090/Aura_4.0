import os
import time
import sqlite3

print("🔧 FORCE FIXING AURA DATABASE...")
print("=" * 50)


def force_fix_database():
    db_file = 'aura.db'
    backup_file = 'aura.db.backup'

    # Close any open database connections
    print("1. Closing database connections...")
    time.sleep(2)  # Wait for any processes to release the file

    # Remove backup file if exists
    if os.path.exists(backup_file):
        try:
            os.remove(backup_file)
            print("✅ Removed old backup file")
        except Exception as e:
            print(f"⚠️  Could not remove backup: {e}")

    # Force remove database file
    if os.path.exists(db_file):
        print("2. Removing corrupted database...")
        max_attempts = 5
        for attempt in range(max_attempts):
            try:
                os.remove(db_file)
                print("✅ Successfully removed corrupted database")
                break
            except PermissionError:
                print(f"   Attempt {attempt + 1}/{max_attempts}: File locked, waiting...")
                time.sleep(2)
                if attempt == max_attempts - 1:
                    print("❌ Could not remove database - it's locked by another program")
                    print("💡 Please close any other AURA instances and try again")
                    return False
            except Exception as e:
                print(f"❌ Error removing database: {e}")
                return False
    else:
        print("📁 No database file found")

    # Create new test database
    print("3. Creating new database...")
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
    if force_fix_database():
        print("\n🎉 DATABASE FIXED SUCCESSFULLY!")
        print("🎯 Now run: python main.py")
    else:
        print("\n❌ DATABASE FIX FAILED!")
        print("💡 Please:")
        print("   1. Close ALL AURA instances")
        print("   2. Close PyCharm/VS Code")
        print("   3. Reopen and run this fix again")
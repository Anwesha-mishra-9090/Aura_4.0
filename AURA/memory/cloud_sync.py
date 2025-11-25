import requests
import json
import os
from datetime import datetime
from utils.config_manager import get_config
from utils.security import encrypt_data, decrypt_data


class CloudSync:
    def __init__(self):
        self.config = get_config()
        self.sync_enabled = self.config.get('cloud_sync', False)
        self.api_key = self.config.get('cloud_api_key', '')
        self.sync_url = "https://api.aura-sync.com"  # Placeholder URL

    def backup_data(self):
        """Backup data to cloud"""
        if not self.sync_enabled or not self.api_key:
            return "Cloud sync disabled or API key not set"

        try:
            # Export local data
            from utils.data_export import export_data
            backup_data = self.get_backup_data()

            # Encrypt sensitive data
            encrypted_data = encrypt_data(json.dumps(backup_data), self.api_key)

            # Upload to cloud (simulated)
            print("📤 Uploading backup to cloud...")

            # Simulate API call
            success = self.simulate_cloud_upload(encrypted_data)

            if success:
                self.update_last_backup()
                return "✅ Cloud backup completed successfully"
            else:
                return "❌ Cloud backup failed"

        except Exception as e:
            return f"❌ Backup error: {e}"

    def restore_data(self):
        """Restore data from cloud"""
        if not self.sync_enabled or not self.api_key:
            return "Cloud sync disabled or API key not set"

        try:
            # Download from cloud (simulated)
            print("📥 Downloading backup from cloud...")
            encrypted_data = self.simulate_cloud_download()

            if not encrypted_data:
                return "❌ No backup found in cloud"

            # Decrypt data
            decrypted_data = decrypt_data(encrypted_data, self.api_key)
            backup_data = json.loads(decrypted_data)

            # Restore to local database
            self.restore_to_database(backup_data)

            return "✅ Cloud restore completed successfully"

        except Exception as e:
            return f"❌ Restore error: {e}"

    def get_backup_data(self):
        """Get all data for backup"""
        from memory.database import get_connection

        conn = get_connection()
        if not conn:
            return {}

        cur = conn.cursor()
        backup = {}

        try:
            # Backup tasks
            cur.execute("SELECT * FROM tasks")
            backup['tasks'] = cur.fetchall()

            # Backup habits
            cur.execute("SELECT * FROM habits")
            backup['habits'] = cur.fetchall()

            # Backup memories
            cur.execute("SELECT * FROM user_memory")
            backup['memories'] = cur.fetchall()

            # Backup configuration
            backup['config'] = get_config()

        finally:
            cur.close()
            conn.close()

        return backup

    def restore_to_database(self, backup_data):
        """Restore data to local database"""
        from memory.database import get_connection

        conn = get_connection()
        if not conn:
            return False

        cur = conn.cursor()

        try:
            # Clear existing data
            cur.execute("DELETE FROM tasks")
            cur.execute("DELETE FROM habits")
            cur.execute("DELETE FROM user_memory")

            # Restore tasks
            for task in backup_data.get('tasks', []):
                cur.execute("INSERT INTO tasks VALUES (?, ?, ?, ?, ?, ?)", task)

            # Restore habits
            for habit in backup_data.get('habits', []):
                cur.execute("INSERT INTO habits VALUES (?, ?, ?, ?, ?, ?)", habit)

            # Restore memories
            for memory in backup_data.get('memories', []):
                cur.execute("INSERT INTO user_memory VALUES (?, ?, ?, ?, ?)", memory)

            conn.commit()
            return True

        except Exception as e:
            print(f"Restore error: {e}")
            return False
        finally:
            cur.close()
            conn.close()

    def simulate_cloud_upload(self, data):
        """Simulate cloud upload (replace with real API call)"""
        print("☁️ Simulating cloud upload...")
        return True

    def simulate_cloud_download(self):
        """Simulate cloud download (replace with real API call)"""
        print("☁️ Simulating cloud download...")
        return json.dumps({"status": "mock_data"})

    def update_last_backup(self):
        """Update last backup timestamp"""
        from utils.config_manager import update_config
        update_config('last_backup', datetime.now().isoformat())

    def get_sync_status(self):
        """Get cloud sync status"""
        return {
            'enabled': self.sync_enabled,
            'last_backup': self.config.get('last_backup', 'Never'),
            'api_key_set': bool(self.api_key)
        }


def enable_cloud_sync(api_key):
    """Enable cloud synchronization"""
    from utils.config_manager import update_config
    update_config('cloud_sync', True)
    update_config('cloud_api_key', api_key)
    return "Cloud sync enabled"


def disable_cloud_sync():
    """Disable cloud synchronization"""
    from utils.config_manager import update_config
    update_config('cloud_sync', False)
    return "Cloud sync disabled"
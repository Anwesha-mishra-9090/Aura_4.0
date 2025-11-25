from datetime import datetime, timedelta
from utils.config_manager import get_config


class CalendarIntegration:
    def __init__(self):
        self.config = get_config()
        self.calendar_enabled = self.config.get('calendar_integration', False)

    def sync_with_calendar(self):
        """Sync tasks with calendar"""
        if not self.calendar_enabled:
            return "Calendar integration disabled"

        try:
            from memory.database import get_connection
            conn = get_connection()
            if not conn:
                return "Database connection failed"

            cur = conn.cursor()

            # Get upcoming tasks
            cur.execute("""
                SELECT task_text, due_date 
                FROM tasks 
                WHERE status = 'pending' 
                AND due_date IS NOT NULL
                ORDER BY due_date ASC
            """)

            tasks = cur.fetchall()
            cur.close()
            conn.close()

            # Create calendar events (simulated)
            events_created = 0
            for task in tasks:
                task_text, due_date = task
                if self.create_calendar_event(task_text, due_date):
                    events_created += 1

            return f"✅ Created {events_created} calendar events"

        except Exception as e:
            return f"❌ Calendar sync error: {e}"

    def create_calendar_event(self, title, due_date):
        """Create a calendar event (simulated)"""
        # This is a simulation - in real implementation, integrate with:
        # - Google Calendar API
        # - Outlook Calendar API
        # - Apple Calendar

        print(f"📅 Creating calendar event: {title} on {due_date}")

        # Simulate API call
        event_data = {
            'title': title,
            'start_time': due_date,
            'end_time': self.calculate_end_time(due_date),
            'description': f'AURA Task: {title}',
            'reminders': ['30 minutes before']
        }

        return self.simulate_calendar_api(event_data)

    def calculate_end_time(self, start_time):
        """Calculate end time for events (1 hour duration)"""
        if isinstance(start_time, str):
            start_time = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
        return start_time + timedelta(hours=1)

    def simulate_calendar_api(self, event_data):
        """Simulate calendar API call"""
        # Replace with actual calendar API integration
        print(f"☁️ Simulating calendar API call for: {event_data['title']}")
        return True

    def get_upcoming_events(self, days=7):
        """Get upcoming calendar events"""
        if not self.calendar_enabled:
            return "Calendar integration disabled"

        # Simulate fetching events
        mock_events = [
            {
                'title': 'Team Meeting',
                'start_time': datetime.now() + timedelta(hours=2),
                'end_time': datetime.now() + timedelta(hours=3),
                'location': 'Conference Room A'
            },
            {
                'title': 'Project Deadline',
                'start_time': datetime.now() + timedelta(days=1),
                'end_time': datetime.now() + timedelta(days=1, hours=1),
                'description': 'Submit final project deliverables'
            }
        ]

        return mock_events

    def sync_calendar_to_tasks(self):
        """Sync calendar events to tasks"""
        if not self.calendar_enabled:
            return "Calendar integration disabled"

        try:
            events = self.get_upcoming_events()
            tasks_created = 0

            for event in events:
                from brain.task_manager import add_task
                task_title = f"Calendar: {event['title']}"
                if add_task(task_title, event['start_time']):
                    tasks_created += 1

            return f"✅ Created {tasks_created} tasks from calendar events"

        except Exception as e:
            return f"❌ Calendar to tasks sync error: {e}"


def enable_calendar_integration():
    """Enable calendar integration"""
    from utils.config_manager import update_config
    update_config('calendar_integration', True)
    return "Calendar integration enabled"


def disable_calendar_integration():
    """Disable calendar integration"""
    from utils.config_manager import update_config
    update_config('calendar_integration', False)
    return "Calendar integration disabled"
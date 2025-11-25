import re
from datetime import datetime, timedelta


def parse_due_date(command):
    """
    Extract due date from natural language
    Returns: datetime object or None
    """
    command = command.lower()

    # Today
    if 'today' in command:
        return datetime.now().replace(hour=18, minute=0, second=0, microsecond=0)

    # Tomorrow
    elif 'tomorrow' in command:
        return (datetime.now() + timedelta(days=1)).replace(hour=18, minute=0, second=0, microsecond=0)

    # Next week
    elif 'next week' in command:
        return datetime.now() + timedelta(days=7)

    # In X days
    days_match = re.search(r'in (\d+) days?', command)
    if days_match:
        days = int(days_match.group(1))
        return datetime.now() + timedelta(days=days)

    # This weekend
    elif 'weekend' in command:
        today = datetime.now()
        days_until_saturday = (5 - today.weekday()) % 7
        return today + timedelta(days=days_until_saturday)

    # Next month
    elif 'next month' in command:
        return datetime.now() + timedelta(days=30)

    # Specific date patterns
    date_match = re.search(r'(\d+)[-/](\d+)[-/]?(\d{2,4})?', command)
    if date_match:
        try:
            day, month, year = date_match.groups()
            year = year or datetime.now().year
            if len(year) == 2:
                year = '20' + year
            return datetime(int(year), int(month), int(day))
        except:
            pass

    return None


def parse_priority(command):
    """
    Extract priority from natural language
    Returns: 3 (high), 2 (medium), 1 (low)
    """
    command = command.lower()

    if any(word in command for word in ['high', 'important', 'urgent', 'critical', 'asap']):
        return 3
    elif any(word in command for word in ['medium', 'normal']):
        return 2
    elif any(word in command for word in ['low', 'not important', 'whenever']):
        return 1
    else:
        return 2


def get_relative_date(days):
    return (datetime.now() + timedelta(days=days)).strftime('%Y-%m-%d')
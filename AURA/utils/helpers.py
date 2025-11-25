import os
from datetime import datetime

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def format_timestamp(timestamp):
    """Format timestamp for display"""
    if isinstance(timestamp, str):
        return timestamp
    return timestamp.strftime('%Y-%m-%d %H:%M')

def get_current_time():
    """Get current time in nice format"""
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def print_banner():
    """Print AURA banner"""
    banner = """
    ╔═══════════════════════════════╗
    ║            A U R A            ║
    ║   Your Personal AI Assistant  ║
    ╚═══════════════════════════════╝
    """
    print(banner)
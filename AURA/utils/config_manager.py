import json
import os

CONFIG_FILE = "aura_config.json"


def get_default_config():
    """Get default configuration"""
    return {
        "openai_api_key": "",
        "user_name": "User",
        "voice_enabled": True,
        "ai_enabled": False,
        "auto_backup": True,
        "theme": "dark",
        "language": "english",
        "productivity_goals": {
            "daily_tasks": 5,
            "weekly_habits": 3,
            "focus_sessions": 4
        }
    }


def get_config():
    """Get current configuration"""
    if not os.path.exists(CONFIG_FILE):
        # Create default config
        default_config = get_default_config()
        save_config(default_config)
        return default_config

    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except:
        return get_default_config()


def save_config(config):
    """Save configuration"""
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)
        return True
    except:
        return False


def update_config(key, value):
    """Update a specific config value"""
    config = get_config()

    # Handle nested keys (e.g., "productivity_goals.daily_tasks")
    if '.' in key:
        keys = key.split('.')
        current = config
        for k in keys[:-1]:
            if k not in current:
                current[k] = {}
            current = current[k]
        current[keys[-1]] = value
    else:
        config[key] = value

    return save_config(config)


def reset_config():
    """Reset to default configuration"""
    default_config = get_default_config()
    return save_config(default_config)
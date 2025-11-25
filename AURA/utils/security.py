import hashlib
import secrets
import json
import os
from datetime import datetime, timedelta

SECURITY_FILE = "aura_security.json"


def hash_password(password):
    """Hash a password for storing"""
    salt = secrets.token_hex(16)
    return hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000).hex() + ':' + salt


def verify_password(password, hashed):
    """Verify a stored password against one provided by user"""
    try:
        stored_hash, salt = hashed.split(':')
        computed_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000).hex()
        return computed_hash == stored_hash
    except:
        return False


def generate_api_key():
    """Generate a secure API key"""
    return secrets.token_urlsafe(32)


def generate_encryption_key():
    """Generate a secure encryption key"""
    return secrets.token_bytes(32)


def encrypt_data_simple(data, key):
    """Simple XOR encryption for demonstration (use proper encryption in production)"""
    # This is a basic example - use proper encryption like AES in production
    encrypted = bytearray()
    key_bytes = key.encode() if isinstance(key, str) else key

    for i, byte in enumerate(data.encode() if isinstance(data, str) else data):
        encrypted.append(byte ^ key_bytes[i % len(key_bytes)])

    return bytes(encrypted)


def decrypt_data_simple(encrypted_data, key):
    """Simple XOR decryption for demonstration"""
    decrypted = bytearray()
    key_bytes = key.encode() if isinstance(key, str) else key

    for i, byte in enumerate(encrypted_data):
        decrypted.append(byte ^ key_bytes[i % len(key_bytes)])

    return bytes(decrypted).decode('utf-8')


def setup_security():
    """Setup basic security configuration"""
    if not os.path.exists(SECURITY_FILE):
        security_config = {
            'api_key': generate_api_key(),
            'encryption_key': generate_encryption_key().hex(),
            'session_timeout': 3600,  # 1 hour
            'max_login_attempts': 5,
            'password_policy': {
                'min_length': 8,
                'require_uppercase': True,
                'require_numbers': True,
                'require_special_chars': True
            },
            'created_at': datetime.now().isoformat()
        }

        with open(SECURITY_FILE, 'w') as f:
            json.dump(security_config, f, indent=2)

        return "Security setup completed"

    return "Security already configured"


def get_security_config():
    """Get security configuration"""
    if not os.path.exists(SECURITY_FILE):
        setup_security()

    try:
        with open(SECURITY_FILE, 'r') as f:
            return json.load(f)
    except:
        return {}


def validate_password_strength(password):
    """Validate password strength"""
    config = get_security_config()
    policy = config.get('password_policy', {})

    if len(password) < policy.get('min_length', 8):
        return False, "Password too short"

    if policy.get('require_uppercase', True) and not any(c.isupper() for c in password):
        return False, "Password must contain uppercase letters"

    if policy.get('require_numbers', True) and not any(c.isdigit() for c in password):
        return False, "Password must contain numbers"

    if policy.get('require_special_chars', True) and not any(not c.isalnum() for c in password):
        return False, "Password must contain special characters"

    return True, "Password is strong"


def audit_log(action, user="system", status="success"):
    """Log security events"""
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'action': action,
        'user': user,
        'status': status,
        'ip_address': '127.0.0.1'  # In real implementation, get from request
    }

    # Append to audit log file
    with open('aura_audit.log', 'a') as f:
        f.write(json.dumps(log_entry) + '\n')


def check_session_timeout(last_activity):
    """Check if session has timed out"""
    timeout_seconds = get_security_config().get('session_timeout', 3600)
    last_activity_time = datetime.fromisoformat(last_activity)
    return datetime.now() - last_activity_time > timedelta(seconds=timeout_seconds)
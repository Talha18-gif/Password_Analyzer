import zxcvbn
import secrets
import string
import random
import sys
import os

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def evaluate_password(password: str) -> dict:
    """
    Evaluates the password strength using the industry-standard zxcvbn library.
    Returns a dictionary containing the score, suggestions, warning, and crack time.
    """
    if not password:
        return {
            'score': 0,
            'score_percentage': 0,
            'suggestions': [],
            'warning': "Please enter a password.",
            'time_to_crack': "instantly",
            'is_common': False
        }

    # Load custom dictionary from common_passwords.txt if it exists
    user_inputs = []
    try:
        dict_path = resource_path('common_passwords.txt')
        with open(dict_path, 'r', encoding='utf-8') as f:
            user_inputs = [line.strip() for line in f if line.strip()]
    except Exception:
        pass

    result = zxcvbn.zxcvbn(password, user_inputs=user_inputs)
    
    score = result['score'] # 0, 1, 2, 3, or 4
    
    # Check if the password was found in our custom common passwords dictionary
    # zxcvbn handles its own dictionary checks, but we want to be explicit if it matches ours.
    is_common = password in user_inputs

    if is_common:
        score = 0

    return {
        'score': score,
        'score_percentage': int((score / 4) * 100),
        'suggestions': result['feedback']['suggestions'],
        'warning': result['feedback']['warning'],
        'time_to_crack': result['crack_times_display']['offline_fast_hashing_1e10_per_second'],
        'is_common': is_common
    }

def generate_strong_password(length=14) -> str:
    """
    Generates a cryptographically strong random password.
    Ensures at least one uppercase, lowercase, digit, and punctuation.
    """
    if length < 4:
        raise ValueError("Minimum length is 4")

    # Ensure at least one character from each category
    categories = [
        secrets.choice(string.ascii_lowercase),
        secrets.choice(string.ascii_uppercase),
        secrets.choice(string.digits),
        secrets.choice(string.punctuation),
    ]
    
    # Fill remaining length with random choices from all categories combined
    all_chars = string.ascii_letters + string.digits + string.punctuation
    for _ in range(length - 4):
        categories.append(secrets.choice(all_chars))

    # Shuffle the characters to prevent predictable patterns
    random.shuffle(categories)
    return ''.join(categories)

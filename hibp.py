import hashlib
import requests

class HIBPAPIError(Exception):
    """Custom exception for Have I Been Pwned API errors."""
    pass

def check_pwned_api(password: str, timeout=10) -> tuple:
    """
    Checks the Have I Been Pwned API to see if a password has been leaked.
    Uses k-anonymity to ensure the password is never sent over the network.
    
    Returns:
        tuple: (total_count, prefix, matched_suffix, matched_count)
    """
    if not password:
        return 0, "", None, 0
        
    sha1_hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    prefix, suffix = sha1_hash[:5], sha1_hash[5:]
    
    url = f'https://api.pwnedpasswords.com/range/{prefix}'
    headers = {'User-Agent': 'PasswordStrengthAnalyzer/2.0 (student project)'}
    
    try:
        resp = requests.get(url, headers=headers, timeout=timeout)
        if resp.status_code != 200:
            raise HIBPAPIError(f"API returned status code: {resp.status_code}")
    except requests.RequestException as e:
        raise HIBPAPIError(f"Network error: {str(e)}")

    matched_suffix = None
    matched_count = 0
    
    for line in resp.text.splitlines():
        if ':' not in line:
            continue
        h, cnt = line.split(':', 1)
        if h == suffix:
            matched_suffix = h
            try:
                matched_count = int(cnt)
            except ValueError:
                matched_count = 1
            break

    total = matched_count
    return total, prefix, matched_suffix, matched_count

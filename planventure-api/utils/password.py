import bcrypt

def hash_password(password: str) -> str:
    """Hash a password using bcrypt and return the hash as a UTF-8 string."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def check_password(password: str, hashed: str) -> bool:
    """Check if a password matches the given bcrypt hash."""
    return bcrypt.checkpw(
        password.encode('utf-8'), 
        hashed.encode('utf-8')
    )
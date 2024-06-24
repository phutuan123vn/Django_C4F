import random
import string

def generate_random_string():
    """Generate a random string of specified length."""
    length = random.randint(8, 12)
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for _ in range(length))
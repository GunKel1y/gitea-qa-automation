import random
import string
from uuid import uuid4

def unique_name(*, prefix: str = "test", length: int = 8) -> str:
    return f"{prefix}_{uuid4().hex[:length]}"

def random_password() -> str:
    return f"test-{str(uuid4())[:10]}-ps-{str(uuid4())[:10]}"

def random_email() -> str:
    return f'test-{str(uuid4())[:15]}@test.ru'

def value_with_length(length: int) -> str:
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def email_with_length(*, length: int, domain: str) -> str:
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length)) + domain

def get_random_color() -> str:
    return f"#{random.randint(0, 0xFFFFFF):06x}"
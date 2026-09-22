import random
import string
from uuid import uuid4


def random_password() -> str:
    return f"test-{str(uuid4())[:10]}-ps-{str(uuid4())[:10]}"

def random_login() -> str:
    return f'user-{str(uuid4())[:7]}'

def random_email() -> str:
    return f'test-{str(uuid4())[:15]}@test.ru'

def password_with_length(length: int) -> str:
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def random_repo_name() -> str:
    return f'repo-{str(uuid4())[:5]}_{str(uuid4())[:5]}'

def repo_name_with_length(length:int):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
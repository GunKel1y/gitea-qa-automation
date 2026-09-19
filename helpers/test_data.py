
from uuid import uuid4


def random_password() -> str:
    return f"test-{str(uuid4())[:10]}-ps-{str(uuid4())[:10]}"

def random_login() -> str:
    return f'user-{str(uuid4())[:7]}'

def random_email() -> str:
    return f'test-{str(uuid4())[:15]}@test.ru'

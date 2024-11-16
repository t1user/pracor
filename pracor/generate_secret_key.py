import os

from django.utils.crypto import get_random_string


def generate():
    SETTINGS_DIR = os.path.abspath(os.path.dirname(__file__))
    chars = "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)"
    key = get_random_string(50, chars)
    with open(os.path.join(SETTINGS_DIR, "secret_key.py"), "w+") as f:
        f.write('SECRET_KEY="' + key + '"')

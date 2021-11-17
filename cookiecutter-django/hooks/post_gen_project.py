import os
import secrets


# https://github.com/django/django/blob/stable/3.2.x/django/core/management/utils.py get_random_secret_key
# https://github.com/django/django/blob/stable/3.2.x/django/utils/crypto.py get_random_string
def get_random_secret_key():
    chars = "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)"
    return "".join(secrets.choice(chars) for i in range(50))


def set_secret_key(path):
    with open(path) as f:
        text = f.read().replace('!!!SECRET_KEY!!!', get_random_secret_key())
    with open(path, 'w') as f:
        f.write(text)


def main():
    set_secret_key(os.path.join("core", "settings.py"))

    if "{{ cookiecutter.use_fathom }}".lower() != "y":
        os.remove(os.path.join("core", "context_processors.py"))


if __name__ == "__main__":
    main()

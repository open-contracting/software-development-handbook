import os
import secrets
from textwrap import dedent


# https://github.com/django/django/blob/stable/3.2.x/django/core/management/utils.py get_random_secret_key
# https://github.com/django/django/blob/stable/3.2.x/django/utils/crypto.py get_random_string
def get_random_secret_key():
    chars = "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)"
    return "".join(secrets.choice(chars) for i in range(50))


def set_secret_key(path):
    with open(path) as f:
        text = f.read().replace("!!!SECRET_KEY!!!", get_random_secret_key())
    with open(path, "w") as f:
        f.write(text)


def use_fathom(enabled):
    if enabled:
        print(
            dedent(
                """
            {%- raw %}
            Run python manage.py startapp and add a fathom.html file to its templates/ directory:

            {% if fathom.id %}
            <script src="https://{{ fathom.domain }}/script.js" data-site="{{ fathom.id }}" defer data-excluded-domains="127.0.0.1,0.0.0.0"></script>
            {% endif %}

            Add before the end of the <head> element in your base template:

            {% include 'fathom.html' %}
            {%- endraw %}
            """  # noqa: E501
            )
        )
    else:
        os.remove(os.path.join("core", "context_processors.py"))


def continuous_deployment(enabled):
    if enabled:
        os.remove(os.path.join(".github", "workflows", "automerge.yml"))


def main():
    set_secret_key(os.path.join("core", "settings.py"))

    use_fathom("{{ cookiecutter.use_fathom }}".lower() == "y")
    continuous_deployment("{{ cookiecutter.continuous_deployment }}".lower() == "y")


if __name__ == "__main__":
    main()

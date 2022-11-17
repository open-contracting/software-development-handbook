from setuptools import find_packages, setup

with open("README.rst") as f:
    long_description = f.read()

setup(
    name="{{ cookiecutter.package_name }}",
    version="0.0.1",
    author="Open Contracting Partnership",
    author_email="data@open-contracting.org",
    url="https://github.com/open-contracting/{{ cookiecutter.repository_name }}",
    description="{{ cookiecutter.short_description }}",
    license="BSD",
    packages=find_packages(exclude=["tests", "tests.*"]),
    long_description=long_description,
    long_description_content_type="text/x-rst",
    install_requires=[
    ],
    extras_require={
        "test": [
            "coveralls",
            "pytest",
            "pytest-cov",
        ],
        "docs": [
            "furo",
            "sphinx",
            "sphinx-autobuild",
        ],
    },
    classifiers=[
        "License :: OSI Approved :: BSD License",
{%- if cookiecutter.os_independent == "y" %}
        "Operating System :: OS Independent",
{%- else %}
        "Operating System :: POSIX :: Linux",
{%- endif %}
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: Implementation :: CPython",
{%- if cookiecutter.pypy == "y" %}
        "Programming Language :: Python :: Implementation :: PyPy",
{%- endif %}
    ],
)

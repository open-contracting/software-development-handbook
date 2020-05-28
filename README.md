# OCP Software Development Handbook

A guide for developers of OCP's tools.

This repository was originally based on OpenDataServices' [sphinx-base](https://github.com/OpenDataServices/sphinx-base). See its [instructions for ReadTheDocs setup](https://github.com/OpenDataServices/sphinx-base#building-on-readthedocs).

## Build and view the documentation

Create and activate a virtual environment, then install requirements:

```shell
pip install -r requirements.txt
```

And build the documentation:

```
cd docs
make html
```

The built documentation is in `_build/html` under `docs`. To view the documentation:

```shell
cd _build/html
python -m http.server
```

And open <http://localhost:8000/> in a browser.

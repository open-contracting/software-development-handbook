# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))
import os

# -- Project information -----------------------------------------------------

project = 'OCP Software Development Handbook'
copyright = '2020, Open Contracting Partnership'
author = 'Open Contracting Partnership'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx_rtd_theme',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = []


# -- Extension configuration -------------------------------------------------

linkcheck_anchors_ignore = [
    # GitHub readme headings.
    r'^(?:change-github-repository-configuration|commit-message-header|tests|unsafe-transforms)$',
]

linkcheck_ignore = [
    # Localhost instructions.
    r'^http://localhost:8000',
    # Redirects to login pages.
    r'^https://(?:crm\.open-contracting\.org|redash\.open-contracting\.org)',
    r'^https://(?:admin\.google\.com|myaccount\.google\.com)/.+',
    r'^https://(?:docs\.google\.com/(?:document|spreadsheets)/d|drive\.google\.com/drive/folders)/.+',
    r'^https://console\.cloud\.google\.com/.+\?organizationId=.+',
    r'^https://groups\.google\.com/a/open-contracting\.org/g/standard-discuss/members\?.+',
    r'^https://(?:app\.usefathom\.com/#|console\.aws\.amazon\.com|readthedocs\.org/dashboard|sentry\.io/settings)/.+',
    r'^https://github\.com/(?:organizations/open-contracting/settings|orgs/open-contracting/teams)/.+',
    r'^https://www\.transifex\.com/.+/collaborators/$',
    r'^https://airtable\.com/.+/workspace/billing$',
    r'^https://pypi\.org/manage/account/#api-tokens$',
    # Redirects to specific versions.
    r'https://docs\.pytest\.org/$',
    r'https://click\.palletsprojects\.com/$',
    r'https://flask\.palletsprojects\.com/$',
    r'https://jinja\.palletsprojects\.com/$',
]

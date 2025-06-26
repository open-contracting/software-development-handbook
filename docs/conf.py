# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "OCP Software Development Handbook"
copyright = "2020, Open Contracting Partnership"
author = "Open Contracting Partnership"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx_design",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "furo"
html_static_path = ["_static"]

# -- Extension configuration -------------------------------------------------

linkcheck_anchors_ignore = [
    # GitHub readme headings.
    r"^(?:change-github-repository-configuration|commit-message-header|github|inputs|node-sass"
    r"|requesting-message-acknowledgements-from-another-thread|tests|unsafe-transforms|L22-L24)$",
]
linkcheck_ignore = [
    # Localhost instructions.
    r"^http://localhost:8000",
    r"^http://127.0.0.1",
    # Returns 404 to linkcheck.
    r"^https://crates.io",
    # Redirects to login pages.
    r"^https://(?:app\.usefathom\.com/#|console\.aws\.amazon\.com|readthedocs\.org/dashboard|sentry\.io/settings)/.+",
    r"^https://(?:admin\.google\.com|myaccount\.google\.com)/.+",
    r"^https://(?:docs\.google\.com/(?:document|spreadsheets)/d|drive\.google\.com/drive/folders)/.+",
    r"^https://console\.cloud\.google\.com/.+\?organizationId=.+",
    r"^https://groups\.google\.com/a/open-contracting\.org/g/standard-discuss/members\?.+",
    r"^https://github\.com/(?:organizations/open-contracting/settings/|orgs/open-contracting/teams|issues/assigned$)",
    r"^https://airtable\.com/.+/workspace/billing$",
    r"^https://coveralls\.io/repos/new$",
    r"^https://pypi\.org/manage/account/#api-tokens$",
    r"^https://readthedocs\.org/dashboard/$",
    r"^https://sentry\.io",
    r"^https://app\.transifex\.com/.+/(collaborators|settings)/$",
    r"^https://cards-dev\.twitter\.com/validator$",
    # Redirects to specific versions.
    r"^https://docs\.pytest\.org/$",
    r"^https://click\.palletsprojects\.com/$",
    r"^https://flask\.palletsprojects\.com/$",
    r"^https://jinja\.palletsprojects\.com/$",
]

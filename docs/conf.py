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

# Sites that render page content with JavaScript, such that no anchor is in the served HTML.
linkcheck_anchors_ignore_for_url = [
    r"^https://github\.com/",
    r"^https://browsersl\.ist/",
    r"^https://www\.rabbitmq\.com/amqp-0-9-1-reference",
]
linkcheck_ignore = [
    # Localhost instructions.
    r"^http://localhost:8000",
    r"^http://127.0.0.1",
    # Returns 400, 403 or 404 to linkcheck.
    r"^https://crates.io",
    r"^https://developers\.facebook\.com/tools/debug/$",
    r"^https://docutils\.sourceforge\.io/",
    r"^https://exercism\.org/tracks/",
    r"^https://medium\.com/",
    r"^https://www\.npmjs\.com/",
    r"^https://status\.lastpass\.com$",
    # Redirects to login pages.
    r"^https://(?:app\.usefathom\.com/#|console\.aws\.amazon\.com|readthedocs\.org/dashboard|sentry\.io/settings)/.+",
    r"^https://admin\.microsoft\.com/#/.+",
    r"^https://dash\.cloudflare\.com/.+",
    r"^https://platform\.securityscorecard\.io/#/.+",
    r"^https://(?:admin\.google\.com|myaccount\.google\.com)/.+",
    r"^https://(?:docs\.google\.com/(?:document|spreadsheets)/d|drive\.google\.com/drive/folders)/.+",
    r"^https://console\.cloud\.google\.com/.+\?organizationId=.+",
    r"^https://groups\.google\.com/a/open-contracting\.org/g/standard-discuss/members\?.+",
    r"^https://github\.com/(?:organizations/open-contracting/settings/|orgs/open-contracting/teams|issues/assigned$|settings/tokens$)",
    r"^https://(?:test\.)?pypi\.org/manage/(?:account/(?:#api-tokens|publishing/)|organization/)",
    r"^https://app\.valimail\.com/app/.+/settings/members$",
    r"^https://(?:accounts|console|konsoleh)\.hetzner\.(?:com|cloud)",
    r"^https://crowdin\.com/profile/.+/managers$",
    r"^https://www\.figma\.com/files/team/.+/members$",
    r"^https://readthedocs\.org/dashboard/$",
    # Redirects to specific versions.
    r"^https://docs\.pytest\.org/$",
    r"^https://click\.palletsprojects\.com/$",
    r"^https://flask\.palletsprojects\.com/$",
    r"^https://jinja\.palletsprojects\.com/$",
]

# CLAUDE.md

Guidance for writing and editing content in the **OCP Software Development Handbook**.

This repository documents the Open Contracting Partnership's (OCP) software-development
policies. The "product" is prose, not code: the content lives in reStructuredText (`.rst`)
files under `docs/`. The goal of this file is to keep new edits consistent with the
existing voice, markup, and structure.

## About this repo

- Sphinx + reStructuredText site. Theme is `furo`; the only extension is `sphinx_design`
  (see `docs/conf.py`). Content lives in `docs/`.
- Built and served on ReadTheDocs (`.readthedocs.yaml`). **The build fails on warnings**,
  so every cross-reference, directive, and link must resolve.
- `cookiecutter-django/` and `cookiecutter-pypackage/` are project templates, excluded from
  linting (`pyproject.toml`). They are not handbook prose — don't apply these style rules to
  them, and don't treat them as examples of the writing style.

## Documentation types and structure

Follow `docs/general/documentation.rst`:

- Know which of the four [Divio documentation types](https://documentation.divio.com) you
  are writing: tutorial, how-to guide, technical reference, or explanation. The type sets
  the page's register, so when it isn't clear from the request or the page you're editing
  (typically for a new page), confirm it with the user before writing. Keep the types on
  separate pages (or at minimum separate sections) and link between them.
- Prefer clarity above all: sacrifice style, flair, brevity, and personality in favor of
  being clear and unambiguous.

## Writing style

- Be **imperative and prescriptive**: "Use X", "Do not Y", "Avoid Z". Address the reader in
  the second person.
- Give the **rationale** where it helps the reader, and acknowledge pragmatic exceptions
  rather than being dogmatic. Rationale almost always lives in body prose, not a boxed
  admonition (a `.. admonition:: Why?` box is rare). Don't force it: terse reference and
  procedure pages often give bare values and steps with no rationale at all.
- **Match the page's register** — the docs span two:
  - *Reference / how-to* pages are terse and operational: an ordered preference list, bare
    config values in a `code-block`, a numbered procedure, a directive table. Don't pad
    these with rationale or decorative admonitions.
  - *Explanation* pages are genuinely discursive — make the argument in flowing prose,
    typically a worked before/after example that narrates *why* the better version is
    better (e.g. the reader's cognitive load), as in `general/code.rst`. Don't reduce these
    to bullet rules.
- How-to guides: give explicit, numbered steps; nest sub-tasks for long lists; omit detail
  that isn't directly relevant; don't include default arguments or other extraneous detail
  in example commands. The setup guide belongs on its own page.
- Use **consistent, specific, non-metaphorical** terms (e.g. "connect to the server", not a
  mix of "go to"/"access the machine"). Link unfamiliar terms to external documentation.
- Refer to the organization as **OCP**; the docs use it unexpanded throughout, so don't
  spell it out. Keep tool names cased consistently: uv, Ruff, Django, pytest, Sphinx, Biome.

## reStructuredText conventions

- **Heading underlines**, in order of nesting: `=` (page title), `-` (section), `~`
  (subsection), `^` (sub-subsection). Headings are noun phrases, not imperative verbs.
  Capitalization is mixed across the docs (both title case and sentence case appear), so
  match the page you are editing.
- **Admonitions** signal the kind of guidance — pick the right one:
  - `.. note::` — clarification or caveat.
  - `.. tip::` — optional optimization.
  - `.. attention::` — a hard requirement.
  - `.. warning::` — a dangerous practice to avoid.
  - `.. admonition:: <Title>` — a custom-titled box for one-off cases (titles seen in the
    docs include `Remember` for must-not-forget guidance, plus `One-time setup`,
    `Reference`, `Complexity rules`).
  - Reserve a short **TLDR** admonition for genuinely dense pages (e.g.
    `python/requirements.rst`). Terse operational pages usually open with one or two bare
    imperative sentences and no admonition at all.
  - Use admonitions deliberately, not decoratively — most pages have only one or two, and
    discursive explanation pages (e.g. `general/code.rst`) use none.
- **Cross-references and links**: use `:doc:` to link pages, `:ref:` to link labeled
  anchors, and `` `text <url>`__ `` for external links. Add a `.. _label:` anchor above a
  section only when another page actually references it. Use `.. seealso::` liberally,
  placed proximate to the relevant section rather than reflexively at the page top. Cite a
  source most often with a trailing one-line `` Reference: `text <url>`__ `` (occasionally a
  `Reference` section or `.. admonition:: Reference`).
- **Code and examples**: use `.. code-block:: <lang>` (e.g. python, bash, toml, yaml);
  shell examples use `sh`/`bash`. Use `none` for non-runnable or illustrative fragments —
  pseudo-code, class/method skeletons, regexes, path globs. Use `.. literalinclude::` to
  pull in a real file when one exists (typically a cookiecutter or sample file); otherwise
  write the example inline as a `code-block`. Show variants (e.g. application vs. package
  config) with `.. tab-set::` / `.. tab-item::`. Use `.. list-table:: :header-rows: 1` for
  tables and before/after comparisons, nesting `code-block`s inside the cells for code
  comparisons.
- **Inline markup**: use double-backtick `` ``code`` `` for filenames, commands, config
  keys, and other literals; use `**strong**` to emphasize must-do words (e.g. **must**,
  **never**) and `*emphasis*` for lighter stress.
- **Lists**: numbered lists for ordered procedures; `-` bullets for non-sequential
  guidance. Use **definition lists** (a term on one line, its explanation indented below)
  for option/preference listings, as in `python/preferences.rst`.

## Reuse existing references

Point to established sources instead of re-explaining them:

- The `cookiecutter-django` and `cookiecutter-pypackage` templates as starting points for
  new projects.
- The `standard-maintenance-scripts` repository for shared tooling and badges.
- The `deploy` repository for deployment code and internal user guides — keep
  deployment-related content there, not duplicated here.

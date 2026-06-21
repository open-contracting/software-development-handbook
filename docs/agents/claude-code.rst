Claude Code
===========

.. seealso::

   -  Anthropic's `Claude Code best practices <https://code.claude.com/docs/en/best-practices>`__ and `how Claude Code works <https://code.claude.com/docs/en/how-claude-code-works>`__
   -  Anthropic's `prompting best practices <https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices>`__
   -  Simon Willison on `coding agents <https://simonwillison.net/2025/Jun/18/coding-agents/>`__
   -  `Agent Skills <https://agentskills.io>`__ (an emerging open standard) and the `CLAUDE.md management plugin <https://claude.com/plugins/claude-md-management>`__

Claude Code is OCP's default coding agent: it runs in a terminal, so it needs no shared editor or IDE, and it gives access to the strongest models. This page is the developer's how-to for using it on OCP's repositories. For guidance that applies to all of Claude's tools — choosing a model, managing context, prompting, and sycophancy — see :doc:`index`.

Choose a project
----------------

Claude Code works best in a project that can check its own work, so prefer a repository:

-  With high **test coverage**. If coverage is low, have the agent add tests first.
-  With **soundness checks**, such as the Rust compiler or a Python type checker. If Python type annotations are missing, have the agent add them first.
-  With strict **linters and formatters**. OCP's default is to enable all rules in Ruff and cargo.

Choose a task
-------------

Choose tasks where **you are the expert**. Do not ask Claude to build or solve something you could not do yourself with your current knowledge: you need to be able to judge the result.

Claude Code is especially good at complex **refactoring**, for example:

-  rewriting contributed code in the style of the rest of the file or project
-  reducing duplication, single-use functions, and single-use or single-letter variables
-  extracting methods

See :doc:`index` for choosing between Claude's tools in the first place.

Set up Claude Code
------------------

Give Claude Code persistent context with a ``CLAUDE.md`` file (see :doc:`index` for how this relates to the context window):

-  A user-level ``~/.claude/CLAUDE.md`` for machine-wide preferences, for example:

   .. code-block:: none

      - Always use `uv` to run Python scripts and manage packages and virtual environments
      - Use `uv run` instead of `python` or `python3`
      - Run `ruff format` after generating code

-  A project ``CLAUDE.md`` for project-specific context: a description of the project (if starting from scratch) and links to relevant documentation, such as the APIs you will use.

Use **plan mode** (press :kbd:`Shift+Tab` to cycle to it) for complex or unfamiliar changes, so Claude explores and proposes a plan before editing. To run Claude Code in a container, use the `devcontainer <https://github.com/anthropics/claude-code/tree/main/.devcontainer>`__.

.. tip::

   Prefer to work **without MCP servers** at first. They are easy to pile on, but each one fills the context with "noise", makes the agent harder to steer, and can duplicate functionality the agent already has — so add one only to solve a real problem you have. When the agent has a terminal, a script or ``Makefile`` it can run is often simpler. Servers that have proven useful include `Playwright <https://github.com/microsoft/playwright-mcp>`__, the `GitHub MCP server <https://github.com/github/github-mcp-server>`__, `Serena <https://github.com/oraios/serena>`__ (a language server), and `Context7 <https://github.com/upstash/context7>`__ (up-to-date dependency documentation). Reference: `MCP <https://code.claude.com/docs/en/mcp>`__.

.. note::

   OCP is on subscription plans, so token cost is not a concern. Out of curiosity, ``npx ccusage`` reports your token usage and the equivalent direct-API cost.

Plan the work
-------------

For a complex request, write a **specification** first, and ask Claude to keep it updated as it makes progress. A cheaper or faster model can do this planning. `This blog post <https://ghuntley.com/specs/>`__ has examples. See :doc:`index` for refining an idea into a prompt before implementing.

Steer the agent
---------------

-  Agents tend to **anchor** to a direction. When you steer Claude off one, delete any code it generated down that path, or it tends to drift back.
-  Work in small steps: **stage** accepted changes with ``git add`` between prompts, and review incremental changes with ``git diff``.
-  Stop Claude with :kbd:`Esc` as soon as it goes off track, then redirect.

.. tip::

   Use `git worktree <https://git-scm.com/docs/git-worktree>`__ so that you and the agent can work on the repository at the same time, independently. See the :doc:`../git/index`.

Work securely and responsibly
-----------------------------

.. seealso::

   :doc:`index` covers the responsibilities that apply to all of Claude's tools. This section covers what is specific to working in a codebase.

Limit permissions
~~~~~~~~~~~~~~~~~~

Keep approval prompts on, and keep ``bypassPermissions`` mode (formerly "dangerously skip permissions") disabled. Add ``permissions.deny`` rules for sensitive paths — at minimum ``pillar/private`` and ``salt/private`` — and remember that the Bash tool can read files such as ``~/.ssh``, so deny what Claude should never see. **Never give the agent access to production.** If you use Claude to debug logs, ensure those logs don't contain security, privacy, or confidential details — the same standard you apply to data sent to Sentry. Administrators manage Claude's GitHub access and enforce organization-wide policy (including disabling ``bypassPermissions`` mode) from the `Claude Code admin settings <https://claude.ai/admin-settings/claude-code>`__. Reference: `Permissions <https://code.claude.com/docs/en/permissions>`__.

Disclose generated code
~~~~~~~~~~~~~~~~~~~~~~~~~

Mark unreviewed AI-generated code so that reviewers and maintainers know what has and hasn't been checked, using all three tags together:

.. code-block:: python

   __generated_by__ = "Claude Code"
   __generated_at__ = "2026-06-21"
   __review_status__ = "unreviewed"

A `PostToolUse hook <https://code.claude.com/docs/en/hooks-guide>`__ can maintain these automatically — refreshing ``__generated_at__`` while a file is still marked ``unreviewed``, and running ``ruff format`` after each edit. A companion ``PreToolUse`` hook can rewrite ``python`` and ``pip`` commands to their ``uv`` equivalents, enforcing the preference in your ``CLAUDE.md``.

It is reasonable to skip thorough review only for low-stakes code: a proof of concept, a prototype, a one-time script, or a non-critical code path. Review anything that reaches a critical path.

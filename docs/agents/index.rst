Claude
======

.. seealso::

   -  Anthropic's `Claude Code best practices <https://code.claude.com/docs/en/best-practices>`__
   -  Anthropic's `prompting best practices <https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices>`__

This page explains how to get good results from Claude — both the chat apps and `Claude Code <https://code.claude.com/docs/en/best-practices>`__ — and how to use it responsibly on OCP's work. These tools change quickly, so treat specific commands and model names as correct at the time of writing, and check the linked official documentation for current details.

If you had a poor experience with these tools, attend office hours before concluding that they don't work for your task: a small change in how you use them often makes the difference.

Task selection
--------------

Claude is most useful on tasks where it can *use tools* — read your files, run commands, search the codebase, and check its own work — rather than answering from memory as a pure language model. Anthropic invests heavily in this tooling, and the results are noticeably better when Claude can act and verify than when it only predicts text. You can tell which mode it is in from the interface: a chat that only writes prose is acting as a language model, whereas a session that reads files, runs commands, and reports what it found is using tools.

Prefer Claude for tasks that have a way to verify the result — a test suite, a build, a screenshot to compare, a script whose output you can check. Give it that check up front, and it can iterate to a working answer instead of stopping at the first plausible one. Reference: `Give Claude a way to verify its work <https://code.claude.com/docs/en/best-practices>`__.

Tools
-----

Match the tool to the task:

-  **Claude apps** (web, desktop, mobile) for chat: questions, drafting, and exploration that don't touch a repository.
-  `Claude Cowork <https://claude.com/product/cowork>`__, in the desktop app, for multi-step knowledge work over your local files and folders — especially working on or searching through long documents. It uses the same agentic approach as Claude Code, without the terminal.
-  **Claude Code** for work in a codebase: reading, editing, running, and committing code. This is the surface most of OCP's development guidance below assumes.
-  `Claude for Microsoft 365 <https://claude.com/claude-for-microsoft-365>`__: add-ins that bring Claude into Word, Excel, PowerPoint, and Outlook, sharing context across your open documents.
-  `Claude Design <https://claude.com/product/design>`__ for visual work: designs, prototypes, slides, and one-pagers.
-  **The Claude browser extension** to act inside your live browser session (for example, a Google Doc).

   .. warning::

      A browser extension operates with *your* live, authenticated session. Treat anything it can reach — email, internal documents, admin consoles — as in scope, and do not point it at confidential or production systems.

.. note::

   These surfaces evolve quickly, and some are in research preview. Confirm the current name, availability, and capabilities of any surface against the `official documentation <https://support.claude.com>`__ before relying on it.

Models
------

Use the most capable model available to you, and the most thorough reasoning setting for demanding work.

-  In the **Claude apps**, select the strongest model in the model picker rather than leaving the default.
-  In **Claude Code**, the ``best`` alias resolves to the most capable model your organization can access; otherwise choose it explicitly with ``/model``. For demanding work, raise the reasoning effort to its highest level with ``/effort`` (for example, ``xhigh`` on current Opus and Fable models). Reference: `Model configuration <https://code.claude.com/docs/en/model-config>`__.

More capable models and higher effort cost more and run slower, so drop to a simpler model or lower effort for routine, low-stakes tasks.

Context
-------

A language model has no memory of its own. Each time you send a message, the model re-reads the **entire** conversation so far — every message, every file or document it has opened, and (in Claude Code) every command's output. That transcript is bounded by a fixed **context window** — roughly 200,000 tokens on most plans, larger on some Enterprise plans — and model performance *degrades as the window fills*: Claude starts to "forget" earlier instructions and make more mistakes. Aim for a high-quality, focused context; a shorter context generally yields better results. Reference: `Usage and length limits <https://support.claude.com/en/articles/11647753-understanding-usage-and-length-limits>`__.

When a conversation approaches the limit, Claude **compacts** it — automatically summarizing older turns to free space and keep going. This happens across the products, including the chat apps and Claude Code, and summarizing can lose detail. So the most reliable habit on any surface is to **start a fresh conversation for an unrelated task**: keep each conversation focused, and carry forward only what matters. The trade-off is that Claude "forgets" the previous thread — see below for how to make starting fresh cheap.

In Claude Code
~~~~~~~~~~~~~~

Claude Code gives you direct control over the context window:

-  See what is using the window with ``/context``, and compact deliberately with ``/compact`` (optionally ``/compact focus on the API changes``) instead of waiting for automatic compaction.
-  Reset the context between unrelated tasks with ``/clear``.
-  Roll back to an earlier, cleaner point with ``/rewind`` (or press ``Esc`` twice) instead of correcting the same mistake repeatedly.
-  For a quick aside that shouldn't bloat the transcript, use ``/btw``.

Persisting context across sessions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Both the apps and Claude Code let you carry context across conversations, so starting fresh is cheap:

-  In the **Claude apps**, a **Project** retains instructions and uploaded files across chats.
-  In **Claude Code**, a ``CLAUDE.md`` file (generate a starting point with ``/init``) gives every session the same project context, and **Skills** load task-specific instructions on demand. These are, in effect, a boilerplate first prompt that is always present — though the harness gives them somewhat higher priority than text you paste in. Reference: `Memory <https://code.claude.com/docs/en/memory>`__.

Either way, keep it lean: an over-long set of instructions or a pile of uploaded documents *adds* noise and reduces the quality of Claude's answers, so don't overdo it.

Two further effects on context apply everywhere:

-  "Thinking" reasoning consumes context, because the model generates reasoning that it then re-reads before answering. Use simpler models or lower effort for simpler tasks.
-  Non-English text reportedly uses more tokens than English for the same content, so it fills the window faster.

Prompting
---------

Provide as much *relevant* detail as is practical up front. A complete first prompt avoids a long back-and-forth that fills the context with corrections and changes of direction, which tends to confuse the model and lower the quality of its output.

That said, do not over-engineer your prompts. You do not need to craft precise, elaborate instructions, pile on memories and skills, or apply "advanced" techniques from self-styled experts: the products already do a great deal of work behind the scenes — system prompts and tooling that Anthropic iterates on continually — and Anthropic's `prompt improver and generator <https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-tools>`__ can refine a draft for you. With experience, you will learn which details matter and which you can leave out.

A few habits that reliably help:

-  Give **example outputs** to follow. Claude is not an oracle; showing the shape of a good answer works better than describing it.
-  If you don't yet know what you're asking for, use one session to refine the idea, then ask Claude to write a clean prompt for a fresh conversation.

Sycophancy
----------

Be wary of sycophancy. Generative models are trained to be agreeable and positive, and there is no reliable way to turn this off. Do not read Claude's enthusiasm as validation of your idea or its own output. When you need a genuine critique, ask for it explicitly, or have a *fresh* session review the work — a separate context that didn't produce the work evaluates it more honestly than the one that did.

Security and responsibility
---------------------------

Risks
~~~~~

The main risks are autonomous operation, over-broad permissions, and exposure of secrets or confidential data — for example, a shell command can read your SSH keys, and a debugging session can pull sensitive values into logs. A subtler, longer-term risk is skill atrophy from delegating work you no longer practice.

Mitigations
~~~~~~~~~~~

Existing OCP practice already covers much of this: secrets are centralized, and ``bypassPermissions`` mode (formerly "dangerously skip permissions") is disabled. Beyond that:

-  **Limit permissions.** Keep approval prompts on, and add ``permissions.deny`` rules for sensitive paths — at minimum ``pillar/private`` and ``salt/private``. Remember that the Bash tool can read files such as ``~/.ssh``, so deny what Claude should never see. Reference: `Permissions <https://code.claude.com/docs/en/permissions>`__.
-  **Never give agents access to production.**
-  **Don't leak through logs.** If you use Claude to debug logs, ensure those logs don't contain security, privacy, or confidential details. They shouldn't already — the same standard you apply to data sent to Sentry.

Responsibility
~~~~~~~~~~~~~~

.. attention::

   You are responsible for code you submit, whether or not Claude wrote it.

Disclose unreviewed AI-generated code — for example, with a ``__generated_by__`` tag or a commit trailer — so reviewers and maintainers know what has and hasn't been checked. It is reasonable to skip thorough review only for low-stakes code: a proof of concept, a prototype, a one-time script, or a non-critical code path. Review anything that reaches a critical path.

Administration
~~~~~~~~~~~~~~

Administrators manage Claude's GitHub access from the `Claude Code admin settings <https://claude.ai/admin-settings/claude-code>`__ and can enforce organization-wide policy (including disabling ``bypassPermissions`` mode) through managed settings. Reference: `Managed settings <https://code.claude.com/docs/en/permissions>`__.

Claude
======

.. seealso::

   -  Anthropic's `Claude Code best practices <https://code.claude.com/docs/en/best-practices>`__
   -  Anthropic's `prompting best practices <https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices>`__

This page explains how to get good results from Claude — both the chat apps and `Claude Code <https://code.claude.com/docs/en/best-practices>`__ — and how to use it responsibly on OCP's work. These tools change quickly, so treat specific commands and model names as correct at the time of writing, and check the linked official documentation for current details.

If you had a poor experience with these tools, attend office hours before concluding that they don't work for your task: a small change in how you use them often makes the difference.

.. admonition:: A mental model: model, context, and tools

   Three things explain most of how these products behave:

   -  the **model** — the LLM that actually generates the response. More capable models reason better; see *Choose the model*.
   -  the **context** — everything the model can see for the current turn: your messages, your instructions, attached files, memory, and the output of any tools it has run. It is bounded by the context window and re-read every turn; see *Manage the context*.
   -  the **tools** — the actions the model can take beyond producing text, such as reading a file, running a shell command, searching the web, or editing code. Tools are what let Claude *act and verify* rather than only predict text.

   Most other features are variations on these three: skills, memory, projects, and ``CLAUDE.md`` shape what is in *context*; MCP servers add *tools*; a subagent is just another bundle of model, context, and tools. Understand these three and the rest follows.

Select your task
----------------

Claude is most useful on tasks where it can *use tools* — read your files, run commands, search the codebase, and check its own work — rather than answering from memory as a pure language model. Anthropic invests heavily in this tooling, and the results are noticeably better when Claude can act and verify than when it only predicts text. You can tell which mode it is in from the interface: a chat that only writes prose is acting as a language model, whereas a session that reads files, runs commands, and reports what it found is using tools.

Prefer Claude for tasks that have a way to verify the result — a test suite, a build, a screenshot to compare, a script whose output you can check. Give it that check up front, and it can iterate to a working answer instead of stopping at the first plausible one. Reference: `Give Claude a way to verify its work <https://code.claude.com/docs/en/best-practices>`__.

Choose the tool
---------------

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

Choose the model
----------------

Use the most capable model available to you, and the most thorough reasoning setting for demanding work.

-  In the **Claude apps**, select the strongest model in the model picker rather than leaving the default.
-  In **Claude Code**, the ``best`` alias resolves to the most capable model your organization can access; otherwise choose it explicitly with ``/model``. For demanding work, raise the reasoning effort to its highest level with ``/effort`` (for example, ``xhigh`` on current Opus and Fable models). Reference: `Model configuration <https://code.claude.com/docs/en/model-config>`__.

More capable models and higher effort cost more and run slower, so drop to a simpler model or lower effort for routine, low-stakes tasks.

Manage the context
-------------------

A language model has no memory of its own. Each time you send a message, the model re-reads the **entire** conversation so far — every message, every file or document it has opened, and (in Claude Code) every command's output. That transcript is bounded by a fixed **context window** — roughly 200,000 tokens on most plans, larger on some Enterprise plans — and model performance *degrades as the window fills*: Claude starts to "forget" earlier instructions and make more mistakes. Aim for a high-quality, focused context; a shorter context generally yields better results. Reference: `Usage and length limits <https://support.claude.com/en/articles/11647753-understanding-usage-and-length-limits>`__.

When a conversation approaches the limit, Claude **compacts** it — automatically summarizing older turns to free space and keep going. This happens across the products, including the chat apps and Claude Code, and summarizing can lose detail. So the most reliable habit on any surface is to **start a fresh conversation for an unrelated task**: keep each conversation focused, and carry forward only what matters. The trade-off is that Claude "forgets" the previous thread; the rest of this section covers what fills the window, what carries over, and how each tool helps.

Claude also manages the window itself, not just you. Compaction is one example; in the agentic tools (Cowork and Claude Code) Claude searches with tools like ``grep`` and reads only the parts of a file it needs rather than loading whole files, and large project knowledge is retrieved on demand. The main thing that is *not* read selectively is a file you attach directly to a chat message, which loads in full (see below).

Files and attachments
~~~~~~~~~~~~~~~~~~~~~~~

How a file reaches the model depends on the tool:

-  In the **chat apps**, a file you attach to a message is read **in full**, so it counts against the context window like pasted text — always present, and costing tokens every turn. (Very large files may instead be handled in Claude's file environment rather than loaded.) Attaching a file inside a Project chat works the same way: it is context for that one conversation, *not* added to the Project's knowledge.
-  In **Cowork** and **Claude Code**, files are read **on demand**: Claude works agentically over the folders you give it access to, opening only the files it needs, so only what it actually reads enters the context.

For a **Project's knowledge** (in the apps and Cowork), Claude loads the whole knowledge base while it is small enough to fit; once it grows past the window, Claude switches to *retrieval*, searching the knowledge and pulling in only the relevant parts. So large project knowledge is searched rather than loaded wholesale. Reference: `RAG for projects <https://support.claude.com/en/articles/11473015-retrieval-augmented-generation-rag-for-projects>`__.

The apps guard against an oversized attachment rather than silently discarding earlier messages: each file is capped (around 30 MB), and if a message and its attachment would exceed the context window, Claude returns a length error and prompts you to shorten the input or start a new chat. References: `Upload files <https://support.claude.com/en/articles/8241126-upload-files-to-claude>`__ (size cap), `Usage and length limits <https://support.claude.com/en/articles/11647753-understanding-usage-and-length-limits>`__, and `Troubleshoot error messages <https://support.claude.com/en/articles/12466728-troubleshoot-claude-error-messages>`__.

Models and thinking
~~~~~~~~~~~~~~~~~~~~

-  "Thinking" reasoning consumes context, because the model generates reasoning that it then re-reads before answering. Use simpler models or lower effort for simpler tasks.
-  The same content can take a different number of tokens depending on the language, so the language you work in affects how quickly the window fills. Reference: `Glossary <https://platform.claude.com/docs/en/about-claude/glossary>`__.

Instructions and projects
~~~~~~~~~~~~~~~~~~~~~~~~~~~

To carry context across conversations in the apps without re-explaining it each time:

-  `Profile instructions <https://support.claude.com/en/articles/10185728-understanding-claude-s-personalization-features>`__ apply to *all* your conversations — your standing profile of who you are and how you like to work.
-  A `Project <https://support.claude.com/en/articles/10185728-understanding-claude-s-personalization-features>`__ bundles standing instructions, a knowledge base, and its own memory for one area of work. Its instructions apply to every chat **within that project**, and a Cowork project can also point at local folders.

Instructions are always present and applied **verbatim**, so keep them lean: an over-long set of instructions *adds* noise and reduces the quality of Claude's answers.

Memory
~~~~~~

`Memory <https://support.claude.com/en/articles/11817273-use-claude-s-chat-search-and-memory-to-build-on-previous-context>`__, when enabled, lets Claude carry context from your past chats. It is **scoped and isolated**: inside a Project, Claude draws only on that Project's own memory — *not* on your account-wide memory from other chats — and your general memory covers only your non-project chats. So something Claude "remembered" in ordinary chats will not be available inside a Project, and vice versa. You add to memory in two ways: by telling Claude in any chat to remember something (for example, "remember that I prefer X"), which it writes into the summary without leaving the conversation and applies from your next chat; or by editing the summary yourself. To read or edit exactly what is stored, open *Settings → Capabilities → View and edit memory*, which lists everything Claude remembers (you can also ask Claude in a chat to show it). The same screen lets you *pause* memory (keep it but stop reading or adding to it) or *reset* it (permanently delete everything, including project memories), and start *incognito* chats that are never remembered.

.. note::

   Instructions are not the same as memory. *You* write instructions, and Claude applies them verbatim to every relevant conversation. **Memory, by contrast, is managed by Claude**: it is a running *summary* of your past chats, not an exact or permanent record. If you ask Claude to remember something, expect it to be reworded, merged with other notes, or eventually dropped as the summary is rewritten. For anything that must persist exactly, write it as a profile or project instruction — or, in Claude Code, in ``CLAUDE.md``. Reference: `Chat search and memory <https://support.claude.com/en/articles/11817273-use-claude-s-chat-search-and-memory-to-build-on-previous-context>`__.

In Claude Code
~~~~~~~~~~~~~~

Claude Code gives you direct control over the context window:

-  See what is using the window with ``/context``, and compact deliberately with ``/compact`` (optionally ``/compact focus on the API changes``) instead of waiting for automatic compaction.
-  Reset the context between unrelated tasks with ``/clear``.
-  Roll back to an earlier, cleaner point with ``/rewind`` (or press ``Esc`` twice) instead of correcting the same mistake repeatedly.
-  For a quick aside that shouldn't bloat the transcript, use ``/btw``.

To carry context across sessions, a ``CLAUDE.md`` file (generate a starting point with ``/init``) gives every session the same project context, and **Skills** load task-specific instructions on demand. These are, in effect, a boilerplate first prompt that is always present — though the harness gives them somewhat higher priority than text you paste in. As with apps instructions, keep them lean. Reference: `Memory <https://code.claude.com/docs/en/memory>`__.

Prompt effectively
------------------

Provide as much *relevant* detail as is practical up front. A complete first prompt avoids a long back-and-forth that fills the context with corrections and changes of direction, which tends to confuse the model and lower the quality of its output.

That said, do not over-engineer your prompts. You do not need to craft precise, elaborate instructions, pile on memories and skills, or apply "advanced" techniques from self-styled experts: the products already do a great deal of work behind the scenes — system prompts and tooling that Anthropic iterates on continually — and Anthropic's `prompt improver and generator <https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-tools>`__ can refine a draft for you. With experience, you will learn which details matter and which you can leave out.

A few habits that reliably help:

-  Give **example outputs** to follow. Claude is not an oracle; showing the shape of a good answer works better than describing it.
-  If you don't yet know what you're asking for, use one session to refine the idea, then ask Claude to write a clean prompt for a fresh conversation.

Watch for sycophancy
--------------------

Be wary of sycophancy. Generative models are trained to be agreeable and positive, and there is no reliable way to turn this off. Do not read Claude's enthusiasm as validation of your idea or its own output. When you need a genuine critique, ask for it explicitly, or have a *fresh* session review the work — a separate context that didn't produce the work evaluates it more honestly than the one that did.

Work securely and responsibly
------------------------------

Claude's main risks are autonomous operation, exposure of secrets or confidential data, and — over the longer term — skill atrophy from delegating work you no longer practice. OCP's existing practices cover much of this: secrets are centralized, and risky "skip all permissions" modes are disabled. Two rules apply on every surface:

-  **Never point Claude at production or confidential systems** — including a browser extension pointed at an authenticated session.
-  **Don't expose confidential data.** Treat anything Claude can read — files, documents, logs — as in scope, and keep secrets, personal data, and confidential details out of what you share.

.. attention::

   You are responsible for whatever you submit, whether or not Claude wrote it.

Disclose unreviewed AI-generated work so that reviewers know what has and hasn't been checked. It is reasonable to skip thorough review only for low-stakes output: a proof of concept, a prototype, a one-time script, or a non-critical code path. Review anything that reaches a critical path.

.. seealso::

   When working in a codebase, see :doc:`claude-code` for OCP's permission and deny rules, the SSH-key caveat, the disclosure tags, and other Claude Code specifics.

.. toctree::
   :hidden:

   Claude Code <claude-code>


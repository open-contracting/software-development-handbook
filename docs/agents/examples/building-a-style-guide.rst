Building a validated CLAUDE.md
==============================

This worked example shows how a ``CLAUDE.md`` style guide for this handbook was produced
through prompting alone, with the author steering an agent rather than hand-editing the
file. The interesting part is not the guide itself but the method used to keep it honest:
the agent's confident-sounding style rules were repeatedly tested against the actual
documentation and corrected wherever they failed.

.. seealso::

   :doc:`../../general/documentation`, for the documentation principles the guide encodes.

The goal was a guide that makes a *future* agent — one without any of this context — write
pages in the handbook's existing voice, markup, and structure. That framing matters,
because it rules out the obvious shortcut of trusting the agent that wrote the guide.

Grounding the guide in the corpus
---------------------------------

The first prompt was deliberately open:

   "Study the documentation content and prepare a CLAUDE.md to ensure future work follows
   the same style as the current content."

The agent explored ``docs/`` and read the handbook's own meta-pages — ``documentation.rst``
and ``contributing.rst`` — before drafting anything, so the guide was anchored in stated
conventions rather than invented ones. The first draft covered the repository setup, the
documentation types, the writing voice, and the reStructuredText conventions.

Pruning to what the agent can act on
------------------------------------

A guide read by an agent should contain only what that agent can observe and apply. Two
prompts cut content that failed this test:

   "You would have no way of knowing this, so I think this section isn't useful."

removed a policy-process section describing an organizational workflow the agent cannot
verify; and a follow-up question about whether two bullets applied to this repository
removed advice that was really meant for the *projects the handbook governs*, not for
editing the handbook. The lesson is to strip aspirational and process content, keeping
guidance the agent can act on directly.

Auditing each claim against the source
--------------------------------------

Every plausible-sounding rule is a hypothesis. One was caught by inspection alone:

   "I don't think this is true: Always expand OCP = Open Contracting Partnership."

A search showed the docs use "OCP" bare throughout and expand it only in build metadata, so
the rule was reversed. That single catch motivated a systematic *conformance audit*: a
sub-agent checked every checkable claim in the guide against the real files, reporting a
verdict and ``file:line`` evidence for each. It found the guide roughly three-quarters
accurate, and two claims outright contradicted — most notably a "one sentence per line"
rule that the prose does not follow. Each finding was corrected, and the one genuine gap it
surfaced (definition lists for option listings) was added.

Testing whether the guide reproduces the style
-----------------------------------------------

A conformance audit answers "do the rules match the corpus?" but not "does *writing from
the rules* reproduce the style?" To test the second question, the agent ran a series of
blind hold-out tests: a fresh sub-agent was given only the guide and a page's heading
skeleton, asked to draft the page, and then — and only then — allowed to read the real page
and diff its draft against it, classifying every difference as a guide gap, a place where
the guide was wrong or over-rigid, or mere authorial freedom.

The first test exposed a problem the audit could not: following the guide produced a
prescriptive essay full of decorative admonitions, where the real page was terse and
operational. The fix was a rule to *match the page's register*. The second test, run on a
genuinely discursive page, showed that the new rule over-corrected — the agent now
under-wrote an explanation page that should read as a flowing argument — so the guidance was
balanced to name both registers explicitly. A third test, on a dense operational page,
confirmed the dominant register now landed.

Each round moved the findings from large (the wrong document shape) to small (where to place
a cross-reference), which is the signature of a converging process rather than an endless
one.

Rejecting findings that don't generalize
-----------------------------------------

An agent's audit findings are themselves hypotheses, so each was checked against the whole
corpus before being adopted. Recommendations that generalized — custom-titled admonitions,
the inline ``Reference:`` line, the ``none`` code-block language — were folded in.
Recommendations that rested on a single page were rejected: a suggestion to "use seealso
sparingly" was dropped once a search found it in most files, and a claimed heading-underline
problem turned out to be a miscount. The author overruled a few remaining cases on intent
the corpus could not reveal:

   "Section anchor labels are only added if actually referenced."

Validating in a clean session
------------------------------

When the guide was ready, the natural next step was to write a real page with it. The
session that *built* the guide is the worst place to do so: its context is saturated with
the style, so it would produce a faithful page whether or not the guide conveys the style.
The honest test is a fresh session in which the guide is the only thing steering the
agent — the same setup as the hold-out tests, with a real task in place of a reconstructed
one.

The reusable recipe
-------------------

- Explore the corpus and anchor the guide in any existing meta-documentation.
- Draft, then prune anything the agent cannot observe or apply.
- Audit every claim against the real files, with citations and counts.
- Run blind hold-out tests across contrasting page types; classify each gap.
- Reject findings that don't generalize; confirm a pattern before adopting it.
- Validate the guide in a clean session, not the one that wrote it.

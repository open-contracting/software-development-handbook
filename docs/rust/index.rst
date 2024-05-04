Rust
====

.. _rust-license:

License
-------

Use the `MIT license <https://choosealicense.com/licenses/mit/>`__.

Development
-----------

-  Install Rust via `rustup <https://rustup.rs>`__ rather than via Homebrew.

Preferences
-----------

-  Prefer crates in the top 250 according to `lib.rs <https://lib.rs/std>`__
-  Read the ``Cargo.toml`` files of OCP projects for inspiration
-  Us unstable features instead of related crates. For example:

   -  `let_chains <https://doc.rust-lang.org/unstable-book/language-features/let-chains.html>`__ instead of `if_chain <https://docs.rs/if_chain/latest/if_chain/>`__
   -  `once_cell <https://doc.rust-lang.org/std/cell/struct.OnceCell.html>`__ instead of `once_cell <https://docs.rs/once_cell/latest/once_cell/>`__ (crate) or `lazy_static <https://docs.rs/lazy_static/latest/lazy_static/>`__
   -  `unix_sigpipe <https://doc.rust-lang.org/beta/unstable-book/language-features/unix-sigpipe.html>`__ instead of `calm_io <https://github.com/myrrlyn/calm_io>`__

.. seealso::

   -  `Serde documentation <https://serde.rs>`__

.. Candidates for preferences https://github.com/open-contracting/cardinal-rs/issues/4

Code style
----------

-  `Avoid matching an Option or Result <https://www.lurklurk.org/effective-rust/transform.html>`__. Instead, use `Option <https://doc.rust-lang.org/std/option/enum.Option.html>`__ and `Result <https://doc.rust-lang.org/std/result/enum.Result.html>`__ methods.
-  `Don't panic <https://www.lurklurk.org/effective-rust/panic.html>`__. This includes ``panic!``, ``unreachable!``, ``unwrap()`` and ``expect()``.
-  Use the same word for macro tokens as for local variables, if appropriate.
-  Use ``super::*`` in ``mod tests`` only. Use ``crate::`` elsewhere.

.. seealso::

   -  `Common Message Styles <https://doc.rust-lang.org/std/error/index.html#common-message-styles>`__

Macros
~~~~~~

Prefer functions, but use macros if you need:

-  Variadic arguments, like ``println!`` or ``vec!``.
-  Code generation at the `item level <https://doc.rust-lang.org/stable/reference/items.html>`__, like creating structs.
-  Code generation at the `expression level <https://doc.rust-lang.org/stable/reference/expressions.html>`__, like accessing struct fields dynamically.

.. seealso::

   -  `The Little Book of Rust Macros <https://veykril.github.io/tlborm/>`__
   -  `Macros <https://doc.rust-lang.org/stable/reference/macros.html>`__ in *The Rust Reference*

   Debugging:

   -  `Debugging <https://veykril.github.io/tlborm/decl-macros/minutiae/debugging.html>`__ in *The Little Book of Rust Macros*
   -  `cargo-expand <https://github.com/dtolnay/cargo-expand>`__
   -  `proc-macro-error <https://crates.io/crates/proc_macro_error>`__

   Crates:

   -  `paste <https://docs.rs/paste/latest/paste/>`__, to use macro arguments to generate identifiers and strings.
   -  To write procedural macros more easily: `quote <https://crates.io/crates/quote>`__, `proc_macro2 <https://crates.io/crates/proc_macro2>`__, `darling <https://crates.io/crates/darling>`__.

Guard clauses
~~~~~~~~~~~~~

Code with too much indentation is hard to read. One option is to use guard clauses. For example:

.. code-block:: rust

   let Some(inner_value) = outer_value else {
       return
   };

.. code-block:: rust

   let inner_value = match outer_value {
       Ok(o) => o,
       Err(e) => return e,
   };

Continuous integration
----------------------

Create a ``.github/workflows/ci.yml`` file. As a base, use:

.. literalinclude:: samples/ci.yml
   :language: yaml

Release process
---------------

#. Ensure that you are on an up-to-date ``main`` branch:

   .. code-block:: bash

      git checkout main
      git pull --rebase

#. Ensure that the package is ready for release:

   -  All tests pass on continuous integration
   -  The version number is correct in ``Cargo.toml``
   -  The changelog is up-to-date and dated

#. Tag the release, replacing ``x.y.z`` twice:

   .. code-block:: bash

      git tag -a x.y.z -m 'x.y.z release.'

#. Push the release:

   .. code-block:: bash

      git push --follow-tags

#. Edit the GitHub release that is created by GitHub Actions, to add the ``description`` value from ``Cargo.toml`` followed by the relevant section of the changelog.

#. If the software has a formula in our `Homebrew tap <https://github.com/open-contracting/homebrew-tap/tree/main/Formula>`__, update the ``url`` and ``sha256`` values. For example, from the ``homebrew-tap`` directory, after updating the ``url`` values, prepare the ``sha256`` values for the ``ocdscardinal`` formula with:

   .. code-block:: bash

      grep --only-matching -E 'https://.+zip' Formula/ocdscardinal.rb | xargs -I{} sh -c 'curl -sSL {} | shasum -a 256'

   Then, push the changes.

#. Publish the crate:

   .. code-block:: bash

      cargo publish

#. Announce on the `discussion group <https://groups.google.com/a/open-contracting.org/g/standard-discuss>`__ if relevant

Development
-----------

Troubleshooting
~~~~~~~~~~~~~~~

If you're getting confusing compile errors, especially any involving type annotations, check that:

-  You wrote enough code. If you produce results that you don't use, the compiler still wants to determine their definite type. Adding more code to give the compiler a hint can spare adding optional type annotations.
-  Your annotations are correct. If you change your code but don't change your annotations, the compiler might report errors that are distantly related to the misannotation.
-  You duck type using trait objects: for example, ``Box<dyn Read>`` to use ``std::io:stdin()`` and ``File::open(file).unwrap()`` interchangeably. The compiler can't determine which traits are relevant across the two types.

If errors relate to ownership, try:

-  Using ``Arc<Mutex<T>>``, as discussed in sections `16.3 <https://doc.rust-lang.org/book/ch16-03-shared-state.html#atomic-reference-counting-with-arct>`__ and `20.2 <https://doc.rust-lang.org/book/ch20-02-multithreaded.html#sending-requests-to-threads-via-channels>`__ of *The Rust Programming Language*.
-  Using ``Option`` with ``take()``, as discussed in sections `17.3 <https://doc.rust-lang.org/book/ch17-03-oo-design-patterns.html#requesting-a-review-of-the-post-changes-its-state>`__ and `20.3 <https://doc.rust-lang.org/book/ch20-03-graceful-shutdown-and-cleanup.html#implementing-the-drop-trait-on-threadpool>`__ of *The Rust Programming Language*.

To reduce the number of allocations, try:

-  Using ``mem::take`` or ``mem::replace`` (`Rust Design Patterns <https://rust-unofficial.github.io/patterns/idioms/mem-replace.html>`__).

.. seealso::

   -  `Winning Fights against the Borrow Checker <https://www.lurklurk.org/effective-rust/borrows.html#winning-fights-against-the-borrow-checker>`__

Learning
~~~~~~~~

Rust has no:

-  `Exception <https://rust-cli.github.io/book/tutorial/errors.html#nicer-error-reporting>`__
-  `Reflection <https://doc.rust-lang.org/book/ch19-06-macros.html#procedural-macros-for-generating-code-from-attributes>`__

Introductions
^^^^^^^^^^^^^

-  `The Rust Programming Language <https://doc.rust-lang.org/book/>`__ (`Moving Captured Values Out of Closures and the Fn Traits <https://doc.rust-lang.org/book/ch13-01-closures.html#moving-captured-values-out-of-the-closure-and-the-fn-traits>`__)
-  `Exercism Rust Track <https://exercism.org/tracks/rust>`__: Read the most upvoted community solution after each exercise.
-  `Unofficial community Discord <https://discord.com/invite/rust-lang-community>`__, in particular ``#rust-help`` and ``#rust-beginners``

.. tip::

   Use `Rust Playground <https://play.rust-lang.org/>`__ to test code snippets.

..
   I prefer Exercism to Rustlings (https://github.com/rust-lang/rustlings). Rustlings' exercises often repeat examples from The Rust Programming Language, and are often solved by the compiler's feedback.

   I don't find it useful to read the examples in Rust by Example (https://doc.rust-lang.org/rust-by-example/), but I occasionally read it when it's a search result.

Topics
^^^^^^

-  `Command line apps in Rust <https://rust-cli.github.io/book/>`__

Memory container cheatsheet
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. image:: https://media.githubusercontent.com/media/usagi/rust-memory-container-cs/master/3840x2160/rust-memory-container-cs-3840x2160-light-back-high-contrast.png
   :class: only-light

.. image:: https://media.githubusercontent.com/media/usagi/rust-memory-container-cs/master/3840x2160/rust-memory-container-cs-3840x2160-dark-back-high-contrast.png
   :class: only-dark

From `usagi/rust-memory-container-cs <https://github.com/usagi/rust-memory-container-cs>`__.

Reference
^^^^^^^^^

-  `The Rust Standard Library <https://doc.rust-lang.org/std/>`__
-  `The Rust Reference <https://doc.rust-lang.org/reference/>`__
-  `docs.rs <https://docs.rs>`__ for crate documentation

   .. tip::

      Scroll up after the page loads to access the within-crate search bar.

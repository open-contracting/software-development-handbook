Rust
====

Development
-----------

-  Install Rust via `rustup <https://rustup.rs>`__ rather than via Homebrew.

Preferences
-----------

-  Prefer crates in the top 250 according to `lib.rs <https://lib.rs/std>`__
-  Read the ``Cargo.toml`` files of OCP projects for inspiration

Troubleshooting
---------------

If you're getting confusing compile errors, especially any involving type annotations, check that:

-  You wrote enough code. If you produce results that you don't use, the compiler still wants to determine their definite type. Adding more code to give the compiler a hint can spare adding optional type annotations.
-  Your annotations are correct. If you change your code but don't change your annotations, the compiler might report errors that are distantly related to the misannotation.
-  You duck type using trait objects: for example, ``Box<dyn Read>`` to use ``std::io:stdin()`` and ``File::open(file).unwrap()`` interchangeably. The compiler can't determine which traits are relevant across the two types.

If errors relate to ownership, try:

-  Using ``Arc<Mutex<T>>``, as discussed in sections `16.3 <https://doc.rust-lang.org/book/ch16-03-shared-state.html#atomic-reference-counting-with-arct>`__ and `20.2 <https://doc.rust-lang.org/book/ch20-02-multithreaded.html#sending-requests-to-threads-via-channels>`__ of *The Rust Programming Language*.
-  Using ``Option`` with ``take()``, as discussed in sections `17.3 <https://doc.rust-lang.org/book/ch17-03-oo-design-patterns.html#requesting-a-review-of-the-post-changes-its-state>`__ and `20.3 <https://doc.rust-lang.org/book/ch20-03-graceful-shutdown-and-cleanup.html#implementing-the-drop-trait-on-threadpool>`__ of *The Rust Programming Language*.

Continuous integration
----------------------

Create a ``.github/workflows/ci.yml`` file. As a base, use:

.. literalinclude:: samples/ci.yml
   :language: yaml

Reference
---------

Read:

-  `The Rust Programming Language <https://doc.rust-lang.org/book/>`__
-  `Command line apps in Rust <https://rust-cli.github.io/book/>`__
-  `The Little Book of Rust Macros <https://veykril.github.io/tlborm/>`__
-  `docs.rs <https://docs.rs>`__ for crate documentation

   .. hint::

      Scroll up after the page loads to access the within-crate search bar

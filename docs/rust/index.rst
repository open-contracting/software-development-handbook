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
-  `docs.rs <https://docs.rs>`__ for crate documentation

   .. hint::

      Scroll up after the page loads to access the within-crate search bar

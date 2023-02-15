Rust
====

Development
-----------

-  Install Rust via `rustup <https://rustup.rs>`__ rather than via Homebrew.

Preferences
-----------

-  Prefer crates in the top 250 according to `lib.rs <https://lib.rs/std>`__
-  Read the ``Cargo.toml`` files of OCP projects for inspiration

Tips & tricks
-------------

-  If one arm of a ``match`` expression for a ``Result`` enum is an identity, use `map <https://doc.rust-lang.org/std/result/enum.Result.html#method.map>`__ or `map_err <https://doc.rust-lang.org/std/result/enum.Result.html#method.map_err>`__ to pass through one variant while handling the other.

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

Reference
---------

Read:

-  `The Rust Programming Language <https://doc.rust-lang.org/book/>`__

   -  `Moving Captured Values Out of Closures and the Fn Traits <https://doc.rust-lang.org/book/ch13-01-closures.html#moving-captured-values-out-of-the-closure-and-the-fn-traits>`__

-  `Command line apps in Rust <https://rust-cli.github.io/book/>`__
-  `The Little Book of Rust Macros <https://veykril.github.io/tlborm/>`__
-  `docs.rs <https://docs.rs>`__ for crate documentation

   .. tip::

      Scroll up after the page loads to access the within-crate search bar

Rust has no:

-  `Exception <https://rust-cli.github.io/book/tutorial/errors.html#nicer-error-reporting>`__
-  `Reflection <https://doc.rust-lang.org/book/ch19-06-macros.html#procedural-macros-for-generating-code-from-attributes>`__

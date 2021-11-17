.dockerignore
=============

The `.dockerignore <https://docs.docker.com/engine/reference/builder/#dockerignore-file>`__ file should only ignore tracked files (not files like ``.DS_Store`` or directories like ``__pycache__``), unless the build generates untracked files (like ``node_modules``).

.. literalinclude:: ../../cookiecutter-django/{{cookiecutter.project_slug}}/.dockerignore
   :language: none

To check the contents of the image, you can run, replacing ``IMAGE``:

.. code-block:: bash

   docker run -it --entrypoint sh IMAGE

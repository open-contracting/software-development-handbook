Continuous integration
======================

Create a ``.github/workflows/docker.yml`` file.

.. note::

   This assumes there is already a :doc:`"CI" workflow <../python/ci>` that runs tests on the ``main`` branch.

If you need to build multiple images, then for each image:

#. Include a ``docker/build-push-action`` step.
#. Set either:

   -  The path to the Dockerfile with the `file <https://github.com/docker/build-push-action#inputs>`__ key
   -  The path to the directory (`context <https://docs.docker.com/engine/context/working-with-contexts/>`__) with the ``context`` key

#. Add a suffix to the repository name under the ``tags`` key.

.. literalinclude:: samples/docker.yml
   :language: yaml

.. note::

   The `docker/build-push-action <https://github.com/docker/build-push-action>`__ step uses `BuildKit <https://docs.docker.com/engine/reference/builder/#buildkit>`__ by default.

..
   The following would simplify the workflow somewhat. However, it would not work when building multiple images, producing an inconsistent approach across repositories.

      # https://github.com/docker/metadata-action#usage
      - uses: docker/metadata-action@v3
        with:
          images: ghcr.io/${{ github.repository }}
          tags: |
            type=ref,event=tag
      # https://github.com/docker/build-push-action#usage
      - uses: docker/build-push-action@v2
        with:
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}

    Note: The docker/metadata-action step with ``type=ref,event=tag`` automatically generates the `latest <https://github.com/docker/metadata-action#latest-tag>`__ tag.

Reference:

-  `Publishing a package using an action <https://docs.github.com/en/packages/managing-github-packages-using-github-actions-workflows/publishing-and-installing-a-package-with-github-actions>`__
-  `Troubleshooting <https://github.com/docker/build-push-action/blob/master/TROUBLESHOOTING.md>`__ ``docker/build-push-action`` step

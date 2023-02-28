Code
====

.. seealso::

   :ref:`principles`

Maintainability over readability
--------------------------------

For example, this code is very readable. Anyone can describe the output.

.. code-block:: python

   print(0)
   print(2)
   print(4)
   print(6)
   print(8)

However, it's not very maintainable. To change the step to 3, you need to change most lines.

Compare:

.. code-block:: python

   for i in range(0, 10, 2):
       print(i)

You only need to change one character. This code is very maintainable, and is less prone to typos.

This may seem obvious, yet repetition like this is very common in outsourced projects.

There are at least these exceptions to `DRY <https://en.wikipedia.org/wiki/Don%27t_repeat_yourself>`__:

-  The duplication is imperfect. Deduplication would involve many branches, which can be harder to read and error-prone.
-  Deduplication would involve nesting loops, which can be harder to read and error-prone.
-  The project is young, and the API is unstable.
-  The repetition is insubstantial.

Avoid paranoid internal APIs
----------------------------

Defensive programming is important for user input. However, for internal APIs, don’t guard against developer error. For example:

-  Using getters and setters to hide attributes.
-  Adding methods to freeze attributes.
-  Asserting that a pre-condition is met.

These protections increase the size of the API. A large API is harder to refactor.

For example, Pelican frontend's tag system had 6 classes and 35 methods before `refactoring <https://github.com/open-contracting/pelican-frontend/commit/dbd97ed>`__, and 7 classes and 23 methods after. The new API is much easier to use, reason about, and edit.

.. list-table::
   :header-rows: 1

   * - Before
     - After
   * - .. code-block:: none

          class Tag:
              def __init__(...):
              def set_param_validation(...):
              def get_param(...):
              def finalize_params(...):
              def validate(...):

          class LeafTag(...):
              def __init__(...):
              def validate_and_process(...):

          class TemplateTag(...):
              def __init__(...):
              def finalize_params(...):
              def set_sub_tag(...):
              def get_sub_tag(...):
              def set_text(...):
              def set_element(...):
              def set_elements(...):
              def get_template_content(...):
              def get_template_styles(...):
              def get_template_fonts(...):
              def merge_template_styles(...):
              def merge_template_fonts(...):
              def merge_template(...):
              def get_tags_mapping(...):
              def validate_and_process(...):

          class TagExpression:
              def __init__(...):
              def process(...):
              def get_tag_name(...):
              def get_tag_params(...):
              def get_tag_count(...):

          class ErrorTag(...):
              def __init__(...):
              def tag_class(...):
                  class ErrorLeafTag(...):
                      def __init__(...):
                      def process_tag(...):
              def process_tag(...):
              def validate(...):
              def prepare_data(...):

          def generate_error_tag(...):

     - .. code-block:: none

           class Tag:
               def __init__(...):
               def set_argument(...):
               def finalize_arguments(...):
               def validate_and_render(...):
               def render(...):

           class LeafTag(...):
               def render(...):

           class TemplateTag(...):
               def __init__(...):
               def get_context(...):
               def get_tags_mapping(...):
               def render(...):

           class Document:
               def __init__(...):
               def get_tags(...):
               def set_text(...):
               def set_element(...):
               def set_elements(...):
               def merge_styles(...):
               def merge_fonts(...):
               def merge(...):

           class TagExpression:
               def parse(...):

           def generate_error_template_tag(...):
               class Tag(...):
                   def get_context(...):

           class ValueTag(...):
               def render(...):

           def xpath(...):

An exception is if the API is very complex. For example, Kingfisher Collect's `BaseSpider <https://github.com/open-contracting/kingfisher-collect/blob/main/kingfisher_scrapy/base_spiders/base_spider.py>`__ has 20+ attributes, some of which can produce an incoherent state. Checking for incoherence and raising an exception is an assist to developers.

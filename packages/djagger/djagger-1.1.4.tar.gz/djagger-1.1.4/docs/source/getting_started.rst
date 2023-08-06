Getting Started
===============

Installation
------------

Install using ``pip``

.. code:: bash

    pip install djagger

Add ``djagger`` to your ``INSTALLED_APPS`` setting in your Django project like this:

.. code:: python

    INSTALLED_APPS = [
        ...
        'djagger',
    ]
  

Include the djagger URLconf in your project ``urls.py`` like this if you want to use the built-in document views.

.. code:: python

    urlpatterns = [
        ...
        path('djagger/', include('djagger.urls')),
    ]

.. NOTE::
   * To see the generated documentation, use the route **/djagger/api/docs**. Djagger uses `Redoc <https://github.com/Redocly/redoc>`_ as the default client generator.       
   * To get the generated JSON schema file, use the route **/djagger/schema.json**.                                                                                           


The path ``djagger/`` is not compulsory when setting this configuration. Replace ``djagger/`` with your preferred route prefix. For customized control over the documentation views, free to remove ``djagger.urls`` and write your own views. The routes provided here are for you to get started quickly.


Package Overview
----------------

Djagger is a pydantic-based Django package that automates the documentation of APIs. The documentation generated is OpenAPI 3 compliant. Djagger seeks to simplify the documentation process while providing a high degree of customization for the generated documentation, all without adding too much bloat to your existing codebase. 

Features
--------

| ✔ OpenAPI 3.0 Compliant
| ✔ Uses pydantic for schema objects
| ✔ Convert Serializers to pydantic models
| ✔ All HTTP methods supported
| ✔ Built-in Views for viewing generated docs
| ✔ Granular customization for individual Views
| ✔ Supports Class-based Views and Function-based Views


**Schema Driven Development** - Use pydantic to generate schema objects to document your Views. Your schemas can in turn be used to validate your requests and responses to ensure that they are consistent with your documentation.


Quickstart
----------

Example GET Endpoint
~~~~~~~~~~~~~~~~~~~~
.. code:: python

    from rest_framework.views import APIView
    from rest_framework.response import Response
    from pydantic import BaseModel as Schema
    import datetime


    class ArticleDetailSchema(Schema):
        created : datetime.datetime
        title : str
        author : str
        content : str


    class RandomArticleAPI(APIView):
        """Return a random article from the Blog"""

        response_schema = ArticleDetailSchema

        def get(self, request):
            ...
            return Response({})

.. raw:: html 

    <p>See the generated docs <a href="https://djagger-example.netlify.app/#tag/Blog/paths/~1blog~1articles~1random/get" target="_blank">here</a>, and the code <a href="https://github.com/royhzq/djagger-example/blob/285af0109155f6ef13e94302a0d40749501388cf/Blog/views.py#L26" target="_blank">here</a>.</p>


Example POST Endpoint
~~~~~~~~~~~~~~~~~~~~~
.. code:: python

    from rest_framework.views import APIView
    from rest_framework.response import Response
    from pydantic import BaseModel as Schema, Field
    import datetime


    class ArticleDetailSchema(Schema):
        created : datetime.datetime
        title : str
        author : str
        content : str

    class ArticleCreateSchema(Schema):
        """POST schema for blog article creation"""
        title : str = Field(description="Title of Blog article")
        content : str = Field(description="Blog article content")


    class ArticleCreateAPI(APIView):

        request_schema = ArticleCreateSchema
        response_schema = ArticleDetailSchema

        def post(self, request):
            ...
            return Response({})

.. raw:: html 

    <p>See the generated docs <a href="https://djagger-example.netlify.app/#tag/Blog/paths/~1blog~1articles~1create/post" target="_blank">here</a>, and the code <a href="https://github.com/royhzq/djagger-example/blob/285af0109155f6ef13e94302a0d40749501388cf/Blog/views.py#L45" target="_blank">here</a>.</p>

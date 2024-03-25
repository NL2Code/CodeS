
Django Solo
===========

Django Solo helps working with singletons: database tables that only have one row. Singletons are useful for things like global settings that you want to edit from the admin instead of having them in Django settings.py.

Features
--------

Solo helps you enforce instantiating only one instance of a model in django.

* You define the model that will hold your singleton object.
* django-solo gives helper parent class for your model and the admin classes.
* You get an admin interface that's aware you only have one object.
* You can retrieve the object from templates.
* By enabling caching, the database is not queried intensively.

Use Cases
--------

Django Solo is also great for use with singleton objects that have a one to many relationship. Like the use case below where you have a 'Home Slider" that has many "Slides".

* Global or default settings
* An image slider that has many slides
* A page section that has sub-sections
* A team bio with many team members

There are many cases where it makes sense for the parent in a one to many relationship to be limited to a single instance.
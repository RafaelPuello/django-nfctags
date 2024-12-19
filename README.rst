================
django-nfctags
================

django-nfctags is a Django app to integrate NFC Tags with a web-based app. Each
NFC Tag will have a unique identifier and a URL that will be opened when the
tag is scanned.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "nfctags" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...,
        "nfctags",
    ]

2. Include the nfctags URLconf in your project urls.py like this::

    path("nfctags/", include("nfctags.urls")),

3. Run ``python manage.py migrate`` to create the models.

4. Start the development server and visit the admin to create an nfctag.

5. Visit the ``/nfctags/`` URL to view your nfctags.
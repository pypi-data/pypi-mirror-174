================
pip-system-certs
================

This package patches pip and requests at runtime to use certificates from the default system store (rather than the bundled certs ca).

This will allow pip to verify tls/ssl connections to servers who's cert is trusted by your system install.

Simply install with::

  pip install pip_system_certs

and pip should trust your https sites if your host os does.

This also extends to all direct uses of the requests library (and other packages that use requests)

PyInstaller
-----------
The method used to automatically enable the cert handling in requests/pip/etc relies on a ``.pth``
file script that python loads at startup. This method does not work when a python application is
bundled into an executable with PyInstaller (or similar).

If you want to use this tool in an application built with PyInstaller it will need to be manually
enabled in your application.

This can be done by adding the following line to the top of your main application script::

    import pip_system_certs.wrapt_requests

This must be run before ``requests`` is imported.

Acknowledgements
----------------
The method of patching at runtime is built from the autowrapt module: https://pypi.python.org/pypi/autowrapt

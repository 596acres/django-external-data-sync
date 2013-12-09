django-external-data-sync
=========================

A simple Django app for periodically locally synchronizing data that is stored 
externally. Sources can be enabled and disabled, or the frequency with which
they should run can be changed, through the Django admin.

`django-external-data-sync` is part of `596 Acres`_' `Living Lots`_ project and
is currently used in `Grounded in Philly`_.

Requirements
------------

Django >= 1.3.1

Installation
------------

Install using pip:

    pip install git+git://github.com/596acres/django-external-data-sync@master

Add to `INSTALLED_APPS`:

    INSTALLED_APPS += (
        'external_data_sync',
    )

Then run `migrate` or `syncdb` on `external_data_sync`.

In `urls.py` add:

    import external_data_sync

    external_data_sync.autodiscover()

For each app that will contain synchronizers, add `synchronizers.py`, subclass 
`synchronizers.Synchronizer`, then register each synchronizer with:

    import external_data_sync

    external_data_sync.register(MySynchronizer)

See `registry.py` for more details.

Finally, use the Django admin to create instances of `SynchronizerRecord`
representing your synchronizers and the frequency with which they should run.
There is a management command, `syncdata`, that will run your synchronizers as
appropriate based on these instances. You will likely want to run `syncdata`
using `cron` or something similar.


License
-------

django-external-data-sync is released under the GNU `Affero General Public 
License, version 3 <http://www.gnu.org/licenses/agpl.html>`_.

.. _`596 Acres`: http://596acres.org/
.. _`Living Lots`: https://github.com/596acres/django-livinglots
.. _`Grounded in Philly`: http://groundedinphilly.org/

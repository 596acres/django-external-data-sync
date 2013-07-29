"""
Tools to maintain a registry of synchronizers.

It looks like this:

- in ``yourapp/synchronizers.py``, register your synchronizers
  with ``external_data_sync.register()``,
- in ``urls.py``, do ``external_data_sync.autodiscover()``

SynchronizerRegistry
    Subclass of Python's dict type with registration/unregistration methods.

registry
    Instance of SynchronizerRegistry.

register
    Proxy registry.register.

autodiscover
    Find synchronizers and fill registry.
"""
from .models import SynchronizerRecord


__all__ = ('SynchronizerRegistry', 'registry', 'register', 'autodiscover')


class SynchronizerRegistry(dict):
    """
    Dict with some shortcuts to handle a registry of synchronizers.
    """

    def unregister(self, name):
        """Unregister a synchronizer."""
        try:
            self[name].delete()
            del self[name]
        except Exception:
            pass

    def register(self, synchronizer):
        """Register a synchronizer."""
        record, created = SynchronizerRecord.objects.get_or_create(
            name=synchronizer.__name__,
            defaults={
                'synchronizer_class': synchronizer.__name__,
                'synchronizer_module': synchronizer.__module__,
            }
        )
        self[synchronizer.__name__] = record


def _autodiscover(registry):
    import copy
    from django.conf import settings
    from django.utils.importlib import import_module
    from django.utils.module_loading import module_has_submodule

    for app in settings.INSTALLED_APPS:
        mod = import_module(app)
        # Attempt to import the app's synchronizers module.
        try:
            before_import_registry = copy.copy(registry)
            import_module('%s.synchronizers' % app)
        except:
            # Reset the model registry to the state before the last import as
            # this import will have to reoccur on the next request and this
            # could raise NotRegistered and AlreadyRegistered exceptions.
            registry = before_import_registry

            # Decide whether to bubble up this error. If the app just
            # doesn't have an admin module, we can ignore the error
            # attempting to import it, otherwise we want it to bubble up.
            if module_has_submodule(mod, 'synchronizers'):
                raise

registry = SynchronizerRegistry()


def autodiscover():
    """
    Check all apps in INSTALLED_APPS for stuff related to external_data_sync.

    For each app, import app.synchronizers if available, resulting in
    execution of register() statements in that module, filling registry.

    Consider a standard app called 'datasource_one' with such a structure::

        datasource_one/
            __init__.py
            models.py
            urls.py
            views.py
            synchronizers.py

    With such a synchronizers.py::

        from external_data_sync import register
        from external_data_sync.synchronizers import Synchronizer

        from .models import DataSourceOne


        class DataSourceOneSynchronizer(Synchronizer):
            pass

        register(DataSourceOne, DataSourceOneSynchronizer)

    When autodiscover() imports datasource_one.synchronizers,
    DataSourceOneSynchronizer will be registered.
    """
    _autodiscover(registry)


def register(*args, **kwargs):
    """Proxy registry.register"""
    return registry.register(*args, **kwargs)

from django.db import models
from django.utils.translation import ugettext_lazy as _

from .synchronizers import do_synchronize


class SynchronizerRecord(models.Model):
    """
    A record of a synchronizer class. Added dynamically by the
    SynchronizerRegistry.
    """

    name = models.CharField(_('name'),
        max_length=128,
        help_text=_('The display name for this synchronizer record.'),
    )

    synchronizer_module = models.CharField(_('synchronizer module'),
        max_length=512,
        help_text=_('The python module where synchronizer_class resides.'),
    )

    synchronizer_class = models.CharField(_('synchronizer class'),
        max_length=512,
        help_text=_('The python class for this synchronizer record.'),
    )

    def __unicode__(self):
        return u'%s' % (self.name,)

    def load(self):
        from django.utils.importlib import import_module

        mod = import_module(self.synchronizer_module)
        return getattr(mod, self.synchronizer_class)


class BaseDataSource(models.Model):
    """
    An external data source that is periodically updated. Will not be updated
    unless a Synchronizer is defined that will do the updating.

    """

    name = models.CharField(_('name'),
        max_length=50,
    )

    description = models.TextField(_('description'),
        blank=True,
        null=True,
    )

    enabled = models.BooleanField(_('enabled'),
        default=True,
    )

    healthy = models.BooleanField(_('healthy'),
        default=True,
        help_text=_('Was synchronizing successful last attempt?'),
    )

    ordering = models.IntegerField(_('ordering'),
        default=1,
        help_text=_('The ordering of this source, lower numbers coming first.'),
    )

    synchronizer_record = models.ForeignKey('SynchronizerRecord',
        verbose_name=_('synchronizer record'),
        blank=True,
        null=True,
        help_text=_('The synchronizer to use with this data source.'),
    )

    synchronize_in_progress = models.BooleanField(_('synchronize in progress'),
        default = False,
        help_text=_('Is the source being synchronized right now?'),
    )

    synchronize_frequency = models.IntegerField(_('synchronize frequency'),
        blank=True,
        null=True,
        help_text=_('The number of hours that should pass between '
                    'synchronizations of this source.'),
    )

    next_synchronize = models.DateTimeField(_('next synchronize'),
        blank=True,
        null=True,
        help_text=_('The next time this data source should be synchronized.'),
    )

    last_synchronized = models.DateTimeField(_('last synchronized'),
        help_text=_('The last time this data source was synchronized'),
    )

    batch_size = models.IntegerField(_('batch size'),
        blank=True,
        null=True,
        help_text=_('The batch size that should be updated each time this '
                    'source is synchronized'),
    )

    def get_synchronizer(self):
        """Instantiate this data source's synchronizer"""
        return self.synchronizer_record.load()(self)

    def synchronize(self):
        do_synchronize(self)

    def __unicode__(self):
        return u'%s' % (self.name,)

    class Meta:
        abstract = True
        ordering = ('ordering',)

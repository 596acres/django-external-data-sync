"""
Infrastructure for periodically synchronizing data sources. Users of this
framework should define a Synchronizer subclass for every DataSource subclass.

"""
from datetime import timedelta
import logging

from django.utils.timezone import now


logger = logging.getLogger(__name__)


def _should_synchronize(data_source):
    if data_source.synchronize_in_progress:
        return False
    if not data_source.next_synchronize:
        return True
    return data_source.next_synchronize < now()


def _update_next_synchronize(data_source):
    if data_source.synchronize_frequency:
        data_source.next_synchronize = now() + timedelta(hours=data_source.synchronize_frequency)
    else:
        data_source.next_synchronize = None
    return data_source


def do_synchronize(data_source):
    if not _should_synchronize(data_source): return
    synchronizer = data_source.get_synchronizer()

    data_source.synchronize_in_progress = True
    data_source.save()

    logger.info('Synchronizing %s' % data_source)
    try:
        synchronizer.sync(data_source)
        data_source.healthy = True
    except Exception:
        logger.exception('Exception while synchronizing %s' % data_source)
        data_source.healthy = False

    data_source = _update_next_synchronize(data_source)
    data_source.synchronize_in_progress = False
    data_source.last_synchronized = now()
    data_source.save()
    logger.info('Done synchronizing %s' % data_source)


class Synchronizer(object):

    def __init__(self, data_source):
        self.data_source = data_source

    def sync(self):
        raise NotImplementedError('Define sync() in all Synchronizers')

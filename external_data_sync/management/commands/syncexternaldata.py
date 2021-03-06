import sys
import traceback

from django.core.management.base import BaseCommand

from ...models import BaseDataSource


class Command(BaseCommand):
    help = 'Synchronize external data sources'

    def handle(self, *args, **options):
        self.stdout.write('sync: Running syncexternaldata')

        for data_source_cls in BaseDataSource.__subclasses__():
            for data_source in data_source_cls.objects.filter(enabled=True):
                print 'sync: Synchronizing %s' % data_source.name
                try:
                    data_source.synchronize()
                except Exception:
                    print 'There was an exception while synchronizing %s' % (
                        data_source,)
                    traceback.print_exc(file=sys.stdout)
                    continue

        self.stdout.write('sync: Done running syncexternaldata')

# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SynchronizerRecord'
        db.create_table(u'external_data_sync_synchronizerrecord', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('synchronizer_module', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('synchronizer_class', self.gf('django.db.models.fields.CharField')(max_length=512)),
        ))
        db.send_create_signal(u'external_data_sync', ['SynchronizerRecord'])


    def backwards(self, orm):
        # Deleting model 'SynchronizerRecord'
        db.delete_table(u'external_data_sync_synchronizerrecord')


    models = {
        u'external_data_sync.synchronizerrecord': {
            'Meta': {'object_name': 'SynchronizerRecord'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'synchronizer_class': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'synchronizer_module': ('django.db.models.fields.CharField', [], {'max_length': '512'})
        }
    }

    complete_apps = ['external_data_sync']
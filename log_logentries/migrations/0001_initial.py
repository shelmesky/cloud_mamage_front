# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Notification'
        db.create_table('log_logentries_notification', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('hostname', self.gf('django.db.models.fields.CharField')(max_length=128, db_index=True)),
            ('state', self.gf('django.db.models.fields.IntegerField')(max_length=1)),
            ('service_description', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('notification_type', self.gf('django.db.models.fields.IntegerField')(max_length=1)),
            ('created_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('output', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('msg_type', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('has_processed', self.gf('django.db.models.fields.IntegerField')(max_length=1, null=True, blank=True)),
        ))
        db.send_create_signal('log_logentries', ['Notification'])


    def backwards(self, orm):
        
        # Deleting model 'Notification'
        db.delete_table('log_logentries_notification')


    models = {
        'log_logentries.notification': {
            'Meta': {'ordering': "['-created_time']", 'object_name': 'Notification'},
            'created_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'has_processed': ('django.db.models.fields.IntegerField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'hostname': ('django.db.models.fields.CharField', [], {'max_length': '128', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'msg_type': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'notification_type': ('django.db.models.fields.IntegerField', [], {'max_length': '1'}),
            'output': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'service_description': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'state': ('django.db.models.fields.IntegerField', [], {'max_length': '1'})
        }
    }

    complete_apps = ['log_logentries']

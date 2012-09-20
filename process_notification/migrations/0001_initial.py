# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Notification_Result'
        db.create_table('process_notification_notification_result', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('from_user', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('to_user', self.gf('django.db.models.fields.CharField')(max_length=128, db_index=True)),
            ('result', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('notification_id', self.gf('django.db.models.fields.IntegerField')(max_length=256)),
            ('message_md5', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('op_processed_result', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
        ))
        db.send_create_signal('process_notification', ['Notification_Result'])


    def backwards(self, orm):
        
        # Deleting model 'Notification_Result'
        db.delete_table('process_notification_notification_result')


    models = {
        'process_notification.notification_result': {
            'Meta': {'ordering': "['-time']", 'object_name': 'Notification_Result'},
            'from_user': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message_md5': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'notification_id': ('django.db.models.fields.IntegerField', [], {'max_length': '256'}),
            'op_processed_result': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'result': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'to_user': ('django.db.models.fields.CharField', [], {'max_length': '128', 'db_index': 'True'})
        }
    }

    complete_apps = ['process_notification']

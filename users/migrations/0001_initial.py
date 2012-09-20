# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Account'
        db.create_table('users_account', (
            ('username', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128, primary_key=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('group_name', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('last_login', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('is_valid', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('date_joined', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('users', ['Account'])


    def backwards(self, orm):
        
        # Deleting model 'Account'
        db.delete_table('users_account')


    models = {
        'users.account': {
            'Meta': {'ordering': "['-date_joined']", 'object_name': 'Account'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'group_name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'is_valid': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128', 'primary_key': 'True'})
        }
    }

    complete_apps = ['users']

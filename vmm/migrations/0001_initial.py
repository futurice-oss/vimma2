# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Schedule'
        db.create_table(u'vmm_schedule', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('startup_time', self.gf('django.db.models.fields.TimeField')(blank=True)),
            ('shutdown_time', self.gf('django.db.models.fields.TimeField')(blank=True)),
            ('days_up', self.gf('django.db.models.fields.CharField')(default='tttttff', max_length=7)),
        ))
        db.send_create_signal(u'vmm', ['Schedule'])

        # Adding model 'VirtualMachine'
        db.create_table(u'vmm_virtualmachine', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('primaryname', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('instance_id', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('updated_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='undefined', max_length=32)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('schedule', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['vmm.Schedule'])),
            ('persist_until', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'vmm', ['VirtualMachine'])


    def backwards(self, orm):
        # Deleting model 'Schedule'
        db.delete_table(u'vmm_schedule')

        # Deleting model 'VirtualMachine'
        db.delete_table(u'vmm_virtualmachine')


    models = {
        u'vmm.schedule': {
            'Meta': {'object_name': 'Schedule'},
            'days_up': ('django.db.models.fields.CharField', [], {'default': "'tttttff'", 'max_length': '7'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'shutdown_time': ('django.db.models.fields.TimeField', [], {'blank': 'True'}),
            'startup_time': ('django.db.models.fields.TimeField', [], {'blank': 'True'})
        },
        u'vmm.virtualmachine': {
            'Meta': {'object_name': 'VirtualMachine'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instance_id': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'persist_until': ('django.db.models.fields.DateTimeField', [], {}),
            'primaryname': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'schedule': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['vmm.Schedule']"}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'undefined'", 'max_length': '32'}),
            'updated_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['vmm']
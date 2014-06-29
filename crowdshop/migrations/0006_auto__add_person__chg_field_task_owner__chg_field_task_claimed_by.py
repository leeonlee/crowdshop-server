# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Person'
        db.create_table(u'crowdshop_person', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('display_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('email', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('token', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
        ))
        db.send_create_signal(u'crowdshop', ['Person'])


        # Changing field 'Task.owner'
        db.alter_column(u'crowdshop_task', 'owner_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['crowdshop.Person']))

        # Changing field 'Task.claimed_by'
        db.alter_column(u'crowdshop_task', 'claimed_by_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['crowdshop.Person']))

    def backwards(self, orm):
        # Deleting model 'Person'
        db.delete_table(u'crowdshop_person')


        # Changing field 'Task.owner'
        db.alter_column(u'crowdshop_task', 'owner_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User']))

        # Changing field 'Task.claimed_by'
        db.alter_column(u'crowdshop_task', 'claimed_by_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['auth.User']))

    models = {
        u'crowdshop.person': {
            'Meta': {'object_name': 'Person'},
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'email': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'token': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        },
        u'crowdshop.task': {
            'Meta': {'ordering': "['-timeStamp']", 'object_name': 'Task'},
            'actual_price': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'claimed_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'claimed_by'", 'null': 'True', 'to': u"orm['crowdshop.Person']"}),
            'complete': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'desc': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tasks'", 'to': u"orm['crowdshop.Person']"}),
            'reward': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'threshold': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'timeStamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['crowdshop']
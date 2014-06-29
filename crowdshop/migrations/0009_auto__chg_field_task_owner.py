# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Task.owner'
        db.alter_column(u'crowdshop_task', 'owner_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['crowdshop.Person']))

    def backwards(self, orm):

        # Changing field 'Task.owner'
        db.alter_column(u'crowdshop_task', 'owner_id', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['crowdshop.Person']))

    models = {
        u'crowdshop.person': {
            'Meta': {'object_name': 'Person'},
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'email': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'token': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        },
        u'crowdshop.state': {
            'Meta': {'object_name': 'State'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'next_state': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'previous_state'", 'unique': 'True', 'null': 'True', 'to': u"orm['crowdshop.State']"})
        },
        u'crowdshop.task': {
            'Meta': {'ordering': "['-timeStamp']", 'object_name': 'Task'},
            'actual_price': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'claimed_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'claimed_by'", 'null': 'True', 'to': u"orm['crowdshop.Person']"}),
            'desc': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tasks'", 'null': 'True', 'to': u"orm['crowdshop.Person']"}),
            'reward': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tasks'", 'to': u"orm['crowdshop.State']"}),
            'threshold': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'timeStamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['crowdshop']
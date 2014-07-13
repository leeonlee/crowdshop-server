# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'MyUser'
        db.create_table(u'crowdshop_myuser', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('is_superuser', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('username', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
            ('is_staff', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('date_joined', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('venmo_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
        ))
        db.send_create_signal(u'crowdshop', ['MyUser'])

        # Adding M2M table for field groups on 'MyUser'
        m2m_table_name = db.shorten_name(u'crowdshop_myuser_groups')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('myuser', models.ForeignKey(orm[u'crowdshop.myuser'], null=False)),
            ('group', models.ForeignKey(orm[u'auth.group'], null=False))
        ))
        db.create_unique(m2m_table_name, ['myuser_id', 'group_id'])

        # Adding M2M table for field user_permissions on 'MyUser'
        m2m_table_name = db.shorten_name(u'crowdshop_myuser_user_permissions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('myuser', models.ForeignKey(orm[u'crowdshop.myuser'], null=False)),
            ('permission', models.ForeignKey(orm[u'auth.permission'], null=False))
        ))
        db.create_unique(m2m_table_name, ['myuser_id', 'permission_id'])

        # Adding model 'State'
        db.create_table(u'crowdshop_state', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('next_state', self.gf('django.db.models.fields.related.OneToOneField')(related_name='previous_state', unique=True, null=True, to=orm['crowdshop.State'])),
        ))
        db.send_create_signal(u'crowdshop', ['State'])

        # Adding model 'Task'
        db.create_table(u'crowdshop_task', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tasks', to=orm['crowdshop.MyUser'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('desc', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('claimed_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='claimed_by', null=True, to=orm['crowdshop.MyUser'])),
            ('threshold', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('actual_price', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('reward', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('timeStamp', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('state', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tasks', to=orm['crowdshop.State'])),
        ))
        db.send_create_signal(u'crowdshop', ['Task'])


    def backwards(self, orm):
        # Deleting model 'MyUser'
        db.delete_table(u'crowdshop_myuser')

        # Removing M2M table for field groups on 'MyUser'
        db.delete_table(db.shorten_name(u'crowdshop_myuser_groups'))

        # Removing M2M table for field user_permissions on 'MyUser'
        db.delete_table(db.shorten_name(u'crowdshop_myuser_user_permissions'))

        # Deleting model 'State'
        db.delete_table(u'crowdshop_state')

        # Deleting model 'Task'
        db.delete_table(u'crowdshop_task')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'crowdshop.myuser': {
            'Meta': {'object_name': 'MyUser'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'venmo_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
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
            'claimed_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'claimed_by'", 'null': 'True', 'to': u"orm['crowdshop.MyUser']"}),
            'desc': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tasks'", 'to': u"orm['crowdshop.MyUser']"}),
            'reward': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tasks'", 'to': u"orm['crowdshop.State']"}),
            'threshold': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'timeStamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['crowdshop']
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.db.models.deletion
import vimma.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Audit',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('timestamp', models.DateTimeField(db_index=True, auto_now_add=True)),
                ('level', models.CharField(max_length=20, choices=[('1-DEBUG', 'DEBUG'), ('2-INFO', 'INFO'), ('3-WARNING', 'WARNING'), ('4-ERROR', 'ERROR')])),
                ('text', models.CharField(max_length=4096)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, blank=True, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AWSProvider',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('access_key_id', models.CharField(max_length=100, blank=True)),
                ('access_key_secret', models.CharField(max_length=100, blank=True)),
                ('ssh_key_name', models.CharField(max_length=50, blank=True)),
                ('route_53_zone', models.CharField(max_length=100, blank=True)),
                ('default_security_group_id', models.CharField(max_length=50, blank=True)),
                ('user_data', models.TextField(blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AWSVM',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('state', models.CharField(max_length=100, blank=True)),
                ('name', models.CharField(max_length=50, validators=[vimma.models.aws_vm_name_validator])),
                ('region', models.CharField(max_length=20)),
                ('security_group_id', models.CharField(max_length=50, blank=True)),
                ('reservation_id', models.CharField(max_length=50, blank=True)),
                ('instance_id', models.CharField(max_length=50, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AWSVMConfig',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('ami_id', models.CharField(max_length=50, blank=True)),
                ('instance_type', models.CharField(max_length=50, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DummyProvider',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DummyVM',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('status', models.CharField(max_length=50, blank=True)),
                ('destroyed', models.BooleanField(default=False)),
                ('poweredon', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DummyVMConfig',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PowerLog',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('powered_on', models.BooleanField(default=None)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100)),
                ('email', models.EmailField(max_length=75)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(unique=True, max_length=50)),
                ('type', models.CharField(max_length=20, choices=[('dummy', 'Dummy'), ('aws', 'Amazon Web Services')])),
                ('max_override_seconds', models.BigIntegerField(default=0)),
                ('is_special', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100)),
                ('permissions', models.ManyToManyField(to='vimma.Permission')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(unique=True, max_length=50)),
                ('matrix', models.TextField(validators=[vimma.models.schedule_matrix_validator])),
                ('is_special', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TimeZone',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VM',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('sched_override_state', models.NullBooleanField(default=None)),
                ('sched_override_tstamp', models.BigIntegerField(null=True, blank=True)),
                ('project', models.ForeignKey(to='vimma.Project', on_delete=django.db.models.deletion.PROTECT)),
                ('provider', models.ForeignKey(to='vimma.Provider', on_delete=django.db.models.deletion.PROTECT)),
                ('schedule', models.ForeignKey(to='vimma.Schedule', on_delete=django.db.models.deletion.PROTECT)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VMConfig',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(unique=True, max_length=50)),
                ('is_special', models.BooleanField(default=False)),
                ('default_schedule', models.ForeignKey(to='vimma.Schedule', on_delete=django.db.models.deletion.PROTECT)),
                ('provider', models.ForeignKey(to='vimma.Provider', on_delete=django.db.models.deletion.PROTECT)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='schedule',
            name='timezone',
            field=models.ForeignKey(to='vimma.TimeZone', on_delete=django.db.models.deletion.PROTECT),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='profile',
            name='projects',
            field=models.ManyToManyField(to='vimma.Project'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='profile',
            name='roles',
            field=models.ManyToManyField(to='vimma.Role'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='powerlog',
            name='vm',
            field=models.ForeignKey(to='vimma.VM'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='dummyvmconfig',
            name='vmconfig',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='vimma.VMConfig'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='dummyvm',
            name='vm',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='vimma.VM'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='dummyprovider',
            name='provider',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='vimma.Provider'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='awsvmconfig',
            name='vmconfig',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='vimma.VMConfig'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='awsvm',
            name='vm',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='vimma.VM'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='awsprovider',
            name='provider',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='vimma.Provider'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='audit',
            name='vm',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='vimma.VM', blank=True, null=True),
            preserve_default=True,
        ),
    ]

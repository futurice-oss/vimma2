# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-09-15 13:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AWSAudit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('level', models.CharField(choices=[('1-DEBUG', 'DEBUG'), ('2-INFO', 'INFO'), ('3-WARNING', 'WARNING'), ('4-ERROR', 'ERROR')], max_length=20)),
                ('text', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AWSFirewallRule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_protocol', models.CharField(choices=[('tcp', 'TCP'), ('udp', 'UDP')], max_length=10)),
                ('from_port', models.PositiveIntegerField()),
                ('to_port', models.PositiveIntegerField()),
                ('cidr_ip', models.CharField(max_length=50)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AWSFirewallRuleExpiration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expires_at', models.DateTimeField()),
                ('last_notification', models.DateTimeField(blank=True, null=True)),
                ('grace_end_action_performed', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AWSPowerLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('powered_on', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AWSProvider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('max_override_seconds', models.BigIntegerField(default=0)),
                ('is_special', models.BooleanField(default=False)),
                ('default', models.BooleanField(default=False)),
                ('access_key_id', models.CharField(blank=True, max_length=100)),
                ('access_key_secret', models.CharField(blank=True, max_length=100)),
                ('ssh_key_name', models.CharField(blank=True, max_length=50)),
                ('route_53_zone', models.CharField(blank=True, max_length=100)),
                ('default_security_group_id', models.CharField(blank=True, max_length=50)),
                ('vpc_id', models.CharField(blank=True, max_length=50, null=True)),
                ('user_data', models.TextField(blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AWSVM',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('sched_override_state', models.NullBooleanField(default=None)),
                ('sched_override_tstamp', models.BigIntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('comment', models.CharField(blank=True, max_length=200)),
                ('status_updated_at', models.DateTimeField(blank=True, null=True)),
                ('destroy_request_at', models.DateTimeField(blank=True, null=True)),
                ('destroyed_at', models.DateTimeField(blank=True, null=True)),
                ('state', models.CharField(blank=True, max_length=100)),
                ('region', models.CharField(default='us-east-1', max_length=20)),
                ('security_group_id', models.CharField(blank=True, max_length=50)),
                ('reservation_id', models.CharField(blank=True, max_length=50)),
                ('instance_id', models.CharField(blank=True, max_length=50)),
                ('ip_address', models.CharField(blank=True, max_length=50)),
                ('private_ip_address', models.CharField(blank=True, max_length=50)),
                ('instance_terminated', models.BooleanField(default=False)),
                ('security_group_deleted', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AWSVMConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('is_special', models.BooleanField(default=False)),
                ('default', models.BooleanField(default=False)),
                ('region', models.CharField(choices=[('ap-northeast-1', 'ap-northeast-1'), ('ap-southeast-1', 'ap-southeast-1'), ('ap-southeast-2', 'ap-southeast-2'), ('cn-north-1', 'cn-north-1'), ('eu-central-1', 'eu-central-1'), ('eu-west-1', 'eu-west-1'), ('sa-east-1', 'sa-east-1'), ('us-east-1', 'us-east-1'), ('us-gov-west-1', 'us-gov-west-1'), ('us-west-1us-west-2', 'us-west-1us-west-2')], default='us-east-1', max_length=20)),
                ('ami_id', models.CharField(blank=True, max_length=50)),
                ('instance_type', models.CharField(blank=True, max_length=50)),
                ('root_device_size', models.IntegerField(default=8)),
                ('root_device_volume_type', models.CharField(choices=[('standard', 'Magnetic'), ('gp2', 'SSD')], default='standard', max_length=20)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AWSVMExpiration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expires_at', models.DateTimeField()),
                ('last_notification', models.DateTimeField(blank=True, null=True)),
                ('grace_end_action_performed', models.BooleanField(default=False)),
                ('vm', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='expiration', to='aws.AWSVM')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

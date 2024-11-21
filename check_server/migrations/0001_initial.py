# Generated by Django 5.1.3 on 2024-11-21 06:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('ssh_port', models.IntegerField(default=22)),
                ('ip', models.CharField(max_length=20)),
                ('username', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=150)),
            ],
            options={
                'unique_together': {('ip', 'username')},
            },
        ),
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_run_on_server', models.CharField(max_length=50)),
                ('port', models.IntegerField(default=0)),
                ('server', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='check_server.server')),
            ],
            options={
                'unique_together': {('port', 'server')},
            },
        ),
        migrations.CreateModel(
            name='Alert',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.TimeField()),
                ('application', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='check_server.application')),
                ('server', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='check_server.server')),
            ],
        ),
    ]
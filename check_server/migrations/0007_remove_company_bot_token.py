# Generated by Django 5.1.3 on 2024-11-23 09:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('check_server', '0006_company_application_company_domain_company_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='bot_token',
        ),
    ]
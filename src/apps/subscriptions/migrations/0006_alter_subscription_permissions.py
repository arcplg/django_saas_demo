# Generated by Django 5.1.3 on 2024-11-30 03:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('subscriptions', '0005_alter_subscription_permissions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='permissions',
            field=models.ManyToManyField(limit_choices_to={'codename__in': ['advanced', 'pro', 'basic', 'basic_ai'], 'content_type__app_label': 'subscriptions'}, to='auth.permission'),
        ),
    ]

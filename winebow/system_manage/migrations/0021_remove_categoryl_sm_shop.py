# Generated by Django 3.2.13 on 2022-05-02 12:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('system_manage', '0020_auto_20220430_1445'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='categoryl',
            name='sm_shop',
        ),
    ]

# Generated by Django 3.2.13 on 2022-04-26 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0004_alter_profile_userphone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='emailVerified',
            field=models.BooleanField(default=False, verbose_name='이메일인증'),
        ),
    ]

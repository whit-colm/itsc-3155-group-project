# Generated by Django 5.0.4 on 2024-05-01 04:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asapp', '0005_thread_date_alter_user_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(default='!YpUTUamYFPKosfmX65r1rVqZIGOFsV5itaxeGOoq', max_length=128),
        ),
    ]
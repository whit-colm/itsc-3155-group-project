# Generated by Django 5.0.4 on 2024-05-04 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asapp', '0004_reporttag_remove_report_message_alter_message_body_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(default='!rEG12JJB9Ulb6jWFmnmP2cKKdc2K3hXrmarags2z', max_length=128),
        ),
    ]

# Generated by Django 4.2.20 on 2025-04-17 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_scanner', '0007_remove_qrcode2_location_remove_qrcode2_person_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='autogenqr',
            name='location',
        ),
        migrations.RemoveField(
            model_name='autogenqr',
            name='person_image',
        ),
        migrations.AddField(
            model_name='loginregister',
            name='location',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='loginregister',
            name='person_image',
            field=models.ImageField(blank=True, null=True, upload_to='person_image/'),
        ),
    ]

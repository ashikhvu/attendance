# Generated by Django 4.2.20 on 2025-04-17 04:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_scanner', '0005_qrcode2_location_qrcode2_person_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='autogenqr',
            name='location',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='autogenqr',
            name='person_image',
            field=models.ImageField(blank=True, null=True, upload_to='person_image/'),
        ),
    ]

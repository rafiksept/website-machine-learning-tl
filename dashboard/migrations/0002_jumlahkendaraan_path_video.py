# Generated by Django 4.2.13 on 2024-06-11 23:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='jumlahkendaraan',
            name='path_video',
            field=models.TextField(default=None),
            preserve_default=False,
        ),
    ]
# Generated by Django 2.2 on 2019-04-14 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venue', '0003_auto_20190414_1001'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venuebooking',
            name='booking_id',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]

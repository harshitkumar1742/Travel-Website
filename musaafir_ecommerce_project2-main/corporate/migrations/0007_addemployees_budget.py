# Generated by Django 3.0.14 on 2022-01-06 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corporate', '0006_auto_20220106_0425'),
    ]

    operations = [
        migrations.AddField(
            model_name='addemployees',
            name='budget',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]